"""Plantilla sin datos: parámetros por ejecución, frescura y sesiones concurrentes."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import create_engine, update
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from app.models import Base, Department, Incident, Role, User
from app.services import incidents
import test_read_query_grouping as reading_tests


class DetailStatementTemplateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = reading_tests.ReadQueryGroupingTests('test_detail_one_query_and_no_sql_when_capturing_dto')
        self.fixture.setUp()
        self.db = self.fixture.db

    def tearDown(self):
        self.fixture.tearDown()

    def test_template_reused_without_bound_identity_or_case_values(self):
        incidents._visible_case_statement.cache_clear()
        first = incidents._visible_case_statement()
        second = incidents._visible_case_statement()
        self.assertIs(first, second)
        self.assertEqual(incidents._visible_case_statement.cache_info().currsize, 1)
        params = first.compile(dialect=postgresql.dialect()).params
        for key in ('detail_actor_id', 'detail_department_id', 'detail_role_id', 'detail_case_id'):
            self.assertIn(key, params)
            self.assertIsNone(params[key])
        self.assertNotIn(self.fixture.actors['admin'].id, params.values())
        self.assertNotIn(self.fixture.cases[0].id, params.values())

    def test_each_execute_gets_new_parameters_for_current_actor_and_case(self):
        actor_one = self.fixture.actors['admin']
        actor_two = self.fixture.actors['outsider']
        first_case, second_case = self.fixture.cases[0], self.fixture.cases[1]
        with patch.object(self.db, 'execute', wraps=self.db.execute) as execute:
            self.assertEqual(incidents.visible_case(self.db, actor_one, first_case.id).id, first_case.id)
            self.assertEqual(incidents.visible_case(self.db, actor_two, second_case.id).id, second_case.id)
        calls = execute.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertIs(calls[0].args[0], calls[1].args[0])
        first, second = calls[0].args[1], calls[1].args[1]
        self.assertIsNot(first, second)
        self.assertEqual(first, {'detail_actor_id': actor_one.id, 'detail_department_id': actor_one.departamento_id,
            'detail_role_id': actor_one.rol_id, 'detail_case_id': first_case.id})
        self.assertEqual(second, {'detail_actor_id': actor_two.id, 'detail_department_id': actor_two.departamento_id,
            'detail_role_id': actor_two.rol_id, 'detail_case_id': second_case.id})

    def test_cached_structure_does_not_cache_authorization_result(self):
        actor = self.fixture.actors['admin']
        case = self.fixture.cases[0]
        self.assertEqual(incidents.visible_case(self.db, actor, case.id).id, case.id)
        case.is_confidential = True
        self.db.commit()
        employee = self.fixture.actors['employee']
        with self.assertRaises(HTTPException) as caught:
            incidents.visible_case(self.db, employee, case.id)
        self.assertEqual(caught.exception.status_code, 404)
        case.is_confidential = False
        self.db.commit()
        self.assertEqual(incidents.visible_case(self.db, employee, case.id).id, case.id)

    def test_role_downgrade_is_honored_after_actor_refresh(self):
        actor = self.fixture.actors['admin']
        case = self.fixture.cases[3]
        self.assertEqual(incidents.visible_case(self.db, actor, case.id).id, case.id)
        self.db.execute(update(User).where(User.id == actor.id).values(rol_id=3),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        self.db.refresh(actor)  # La autenticación ya refresca al actor por petición.
        with self.assertRaises(HTTPException) as caught:
            incidents.visible_case(self.db, actor, case.id)
        self.assertEqual(caught.exception.status_code, 404)

    def test_current_role_name_still_read_after_template_warmup(self):
        actor = self.fixture.actors['admin']
        case = self.fixture.cases[0]
        self.assertEqual(incidents.visible_case(self.db, actor, case.id).id, case.id)
        self.db.execute(update(Role).where(Role.id == 1).values(nombre='NO_HABILITADO'),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        with self.assertRaises(HTTPException) as caught:
            incidents.visible_case(self.db, actor, case.id)
        self.assertEqual((caught.exception.status_code, caught.exception.detail), (403, 'Rol no habilitado'))

    def test_concurrent_sessions_do_not_mix_actor_or_case_parameters(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            engine = create_engine('sqlite:///' + str(Path(folder) / 'ficticio.db'),
                                   connect_args={'check_same_thread': False})
            Base.metadata.create_all(engine)
            try:
                with Session(engine) as setup:
                    setup.add(Role(id=3, nombre='EMPLEADO'))
                    department = Department(nombre='Concurrente ficticio', is_active=True)
                    setup.add(department); setup.flush()
                    users = [User(email=f'template-{index}@example.invalid', nombre_completo='Ficticio',
                        rol_id=3, departamento_id=department.id, is_active=True) for index in range(2)]
                    setup.add_all(users); setup.flush()
                    cases = [Incident(titulo='Ficticio', descripcion='Ficticio', scope='ENTORNO',
                        incident_date=self.fixture.cases[0].incident_date, created_by=user.id,
                        reported_department_id=department.id, department_id_at_creation=department.id,
                        is_confidential=False) for user in users]
                    setup.add_all(cases); setup.flush()
                    identities = [(user.id, case.id) for user, case in zip(users, cases)]
                    setup.commit()
                barrier = threading.Barrier(2)
                incidents._visible_case_statement.cache_clear()
                def read(index):
                    user_id, own_case = identities[index]
                    other_case = identities[1-index][1]
                    with Session(engine) as db:
                        actor = db.get(User, user_id)
                        barrier.wait(timeout=5)
                        for _ in range(3):
                            if incidents.visible_case(db, actor, own_case).id != own_case:
                                return False
                            try:
                                incidents.visible_case(db, actor, other_case)
                            except HTTPException as error:
                                if error.status_code != 404:
                                    return False
                            else:
                                return False
                    return True
                with ThreadPoolExecutor(max_workers=2) as pool:
                    futures = [pool.submit(read, index) for index in range(2)]
                    self.assertEqual([future.result(timeout=10) for future in futures], [True, True])
            finally:
                engine.dispose()


if __name__ == '__main__':
    unittest.main()
