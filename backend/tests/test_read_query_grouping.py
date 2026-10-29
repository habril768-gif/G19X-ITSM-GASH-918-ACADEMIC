"""Paginación agrupada y detalle autorizado: resultados, límites y viajes SQL."""
from contextlib import contextmanager
from datetime import date, datetime, timezone
import inspect
import unittest
from uuid import UUID

from fastapi import HTTPException, Response
from sqlalchemy import create_engine, event, select, update
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from app.api.incidents import CaseDetail, CasePage, list_cases
from app.models import Base, Department, Incident, IncidentParticipant, Role, User
from app.services.incidents import visible_case, visibility


class ReadQueryGroupingTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine, expire_on_commit=False)
        self.db.add_all([Role(id=1, nombre='ADMIN_RH'), Role(id=2, nombre='SUPERVISOR'), Role(id=3, nombre='EMPLEADO')])
        self.one = Department(nombre='Uno ficticio', is_active=True)
        self.two = Department(nombre='Dos ficticio', is_active=True)
        self.db.add_all([self.one, self.two]); self.db.flush()
        self.actors = {}
        for name, role, department in [('admin', 1, self.one), ('admin2', 1, self.two),
                ('super', 2, self.one), ('super2', 2, self.two), ('employee', 3, self.one),
                ('peer', 3, self.one), ('outsider', 3, self.two)]:
            self.actors[name] = User(email=name+'@example.invalid', nombre_completo='Ficticio',
                                    rol_id=role, departamento_id=department.id, is_active=True)
        self.db.add_all(list(self.actors.values())); self.db.flush()
        self.cases = []
        for index, (scope, creator, affected, department, confidential) in enumerate([
            ('ENTORNO', 'employee', None, self.one, False),
            ('ENTORNO', 'outsider', None, self.two, False),
            ('ENTORNO', 'employee', None, self.one, True),
            ('PERSONA', 'employee', 'employee', self.one, False),
            ('PERSONA', 'employee', 'super', self.one, False),
            ('ENTORNO', 'employee', None, self.one, False),
            ('ENTORNO', 'peer', None, self.one, False),
            ('PERSONA', 'peer', 'peer', self.one, False),
        ]):
            case = Incident(id=UUID(int=index+1), titulo='literal %' if index == 6 else f'Ficticio {index}',
                descripcion='Datos ficticios', scope=scope, created_by=self.actors[creator].id,
                affected_employee_id=self.actors[affected].id if affected else None,
                reported_department_id=department.id, department_id_at_creation=department.id,
                incident_date=date(2026, 10, 22), is_confidential=confidential,
                category_id=4 if scope == 'ENTORNO' else None,
                created_at=datetime(2026, 10, 22, 12, tzinfo=timezone.utc))
            self.cases.append(case)
        self.db.add_all(self.cases); self.db.flush()
        self.db.add(IncidentParticipant(incidencia_id=self.cases[5].id,
            user_id=self.actors['admin'].id, declaration_reason='Ficticio', review_status='DECLARADO'))
        self.db.commit()
        self.list_source = inspect.unwrap(list_cases)

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def page(self, actor='admin', **extra):
        args = dict(response=Response(), page=1, page_size=20, status=None, priority=None,
            category_id=None, assigned_to=None, created_from=None, created_to=None, q=None,
            user=self.actors[actor], db=self.db)
        args.update(extra)
        return self.list_source(**args)

    @contextmanager
    def queries(self):
        values = []
        def observe(conn, cursor, statement, parameters, context, executemany):
            values.append((statement, context.compiled.statement))
        event.listen(self.engine, 'before_cursor_execute', observe)
        try:
            yield values
        finally:
            event.remove(self.engine, 'before_cursor_execute', observe)

    def test_list_two_queries_and_no_sql_when_capturing_dto(self):
        with self.queries() as queries:
            result = self.page()
            before = len(queries)
            model = CasePage.model_validate(result)
            self.assertEqual(len(queries), before)
        self.assertEqual(len(queries), 2)  # rol + count/página; sin autenticación
        self.assertEqual(model.total, 7)
        self.assertIn('LEFT OUTER JOIN', queries[-1][0])

    def test_empty_filter_retains_total_zero_and_empty_items(self):
        result = self.page(q='inexistente')
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['items'], [])

    def test_page_out_of_range_retains_nonzero_total(self):
        result = self.page(page=99, page_size=2)
        self.assertEqual(result['total'], 7)
        self.assertEqual(result['items'], [])
        self.assertEqual((result['page'], result['page_size']), (99, 2))

    def test_stable_tied_order_and_no_duplicated_items_across_pages(self):
        ids = []
        for page in (1, 2, 3):
            result = self.page(page=page, page_size=3)
            self.assertEqual(result['total'], 7)
            ids.extend(case.id for case in result['items'])
        expected = sorted([case.id for index, case in enumerate(self.cases) if index != 5], reverse=True)
        self.assertEqual(ids, expected)
        self.assertEqual(len(ids), len(set(ids)))

    def test_list_matches_legacy_predicate_for_all_roles_and_departments(self):
        for name, actor in self.actors.items():
            with self.subTest(actor=name):
                expected = set(self.db.scalars(select(Incident.id).where(visibility(self.db, actor))))
                result = self.page(actor=name)
                self.assertEqual(result['total'], len(expected))
                self.assertEqual({case.id for case in result['items']}, expected)

    def test_literal_search_category_and_dates_use_same_authorized_total(self):
        result = self.page(q='%', category_id=4,
            created_from=date(2026, 10, 22), created_to=date(2026, 10, 22))
        self.assertEqual(result['total'], 1)
        self.assertEqual([case.id for case in result['items']], [self.cases[6].id])
        self.assertEqual(self.page(created_to=date(2026, 10, 21))['total'], 0)
        with self.assertRaises(HTTPException) as caught:
            self.page(created_from=date(2026, 10, 23), created_to=date(2026, 10, 22))
        self.assertEqual(caught.exception.status_code, 422)

    def test_detail_one_query_and_no_sql_when_capturing_dto(self):
        with self.queries() as queries:
            case = visible_case(self.db, self.actors['admin'], self.cases[0].id)
            before = len(queries)
            model = CaseDetail.model_validate(case)
            self.assertEqual(len(queries), before)
        self.assertEqual(len(queries), 1)  # rol + caso; sin autenticación
        self.assertEqual(model.id, self.cases[0].id)

    def test_detail_matches_legacy_authorization_matrix(self):
        for name, actor in self.actors.items():
            for case in self.cases:
                with self.subTest(actor=name, case=str(case.id)):
                    expected = self.db.scalar(select(Incident.id).where(
                        Incident.id == case.id, visibility(self.db, actor)))
                    if expected is None:
                        with self.assertRaises(HTTPException) as caught:
                            visible_case(self.db, actor, case.id)
                        self.assertEqual(caught.exception.status_code, 404)
                    else:
                        self.assertEqual(visible_case(self.db, actor, case.id).id, expected)

    def test_detail_unknown_or_missing_role_is_403_even_without_case(self):
        actor = self.actors['admin']
        cached = self.db.get(Role, 1)
        self.db.execute(update(Role).where(Role.id == 1).values(nombre='NO_HABILITADO'),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        self.assertEqual(cached.nombre, 'ADMIN_RH')
        for case_id in (self.cases[0].id, UUID(int=999)):
            with self.assertRaises(HTTPException) as caught:
                visible_case(self.db, actor, case_id)
            self.assertEqual((caught.exception.status_code, caught.exception.detail), (403, 'Rol no habilitado'))
        actor.rol_id = 99
        self.db.commit()
        with self.assertRaises(HTTPException) as caught:
            visible_case(self.db, actor, UUID(int=999))
        self.assertEqual(caught.exception.status_code, 403)

    def test_detail_missing_case_remains_404_for_valid_role(self):
        with self.assertRaises(HTTPException) as caught:
            visible_case(self.db, self.actors['admin'], UUID(int=999))
        self.assertEqual((caught.exception.status_code, caught.exception.detail), (404, 'Incidencia no encontrada'))

    def test_grouped_statements_compile_for_postgresql(self):
        with self.queries() as queries:
            self.page()
            visible_case(self.db, self.actors['super'], self.cases[0].id)
        statements = [str(expression.compile(dialect=postgresql.dialect())) for _, expression in queries]
        self.assertIn('LEFT OUTER JOIN', statements[-2])
        self.assertIn('LEFT OUTER JOIN incidencias', statements[-1])
        self.assertIn('roles.nombre', statements[-1])


if __name__ == '__main__':
    unittest.main()
