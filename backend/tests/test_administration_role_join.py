"""Rol fresco en relectura conjunta, orden de lock y compatibilidad previa."""
from types import SimpleNamespace
import unittest

from fastapi import HTTPException
from sqlalchemy import create_engine, delete, event, update
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import TextClause

from app.models import Base, Department, Role, User
from app.services.administration_lock import administration_lock


class AdministrationRoleJoinTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine, expire_on_commit=False)
        self.db.add_all([Role(id=1, nombre='ADMIN_RH'), Role(id=2, nombre='SUPERVISOR'), Role(id=3, nombre='EMPLEADO')])
        self.department = Department(nombre='Ficticio', is_active=True)
        self.db.add(self.department); self.db.flush()
        self.actor = User(email='join@example.invalid', nombre_completo='Ficticio', rol_id=1,
                          departamento_id=self.department.id, is_active=True)
        self.db.add(self.actor); self.db.commit()
        self.sql = []
        self.observe = lambda conn, cursor, statement, parameters, context, executemany: self.sql.append(statement)
        event.listen(self.engine, 'before_cursor_execute', self.observe)

    def tearDown(self):
        event.remove(self.engine, 'before_cursor_execute', self.observe)
        self.db.close()
        self.engine.dispose()

    def test_role_returns_in_single_join_and_actor_refreshes(self):
        self.db.execute(update(User).where(User.id == self.actor.id).values(rol_id=3),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        self.assertEqual(self.actor.rol_id, 1)
        self.sql.clear()
        self.assertEqual(administration_lock(self.db, self.actor, include_role=True), 'EMPLEADO')
        self.assertEqual(self.actor.rol_id, 3)
        self.assertEqual(len(self.sql), 1)
        self.assertIn('JOIN roles', self.sql[0])

    def test_no_role_cache_between_calls(self):
        self.assertEqual(administration_lock(self.db, self.actor, include_role=True), 'ADMIN_RH')
        self.db.execute(update(User).where(User.id == self.actor.id).values(rol_id=2),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        self.sql.clear()
        self.assertEqual(administration_lock(self.db, self.actor, include_role=True), 'SUPERVISOR')
        self.assertEqual(len(self.sql), 1)

    def test_role_name_refresh_ignores_stale_role_object(self):
        cached = self.db.get(Role, 1)
        self.db.execute(update(Role).where(Role.id == 1).values(nombre='NO_HABILITADO'),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        self.assertEqual(cached.nombre, 'ADMIN_RH')
        self.sql.clear()
        with self.assertRaises(HTTPException) as caught:
            administration_lock(self.db, self.actor, include_role=True)
        self.assertEqual((caught.exception.status_code, caught.exception.detail), (403, 'Rol no habilitado'))
        self.assertEqual(len(self.sql), 1)

    def test_missing_role_preserves_role_error(self):
        self.db.execute(delete(Role).where(Role.id == 1), execution_options={'synchronize_session': False})
        self.db.commit()
        self.sql.clear()
        with self.assertRaises(HTTPException) as caught:
            administration_lock(self.db, self.actor, include_role=True)
        self.assertEqual((caught.exception.status_code, caught.exception.detail), (403, 'Rol no habilitado'))
        self.assertEqual(len(self.sql), 1)

    def test_inactive_department_still_denies_before_role_return(self):
        self.db.execute(update(Department).where(Department.id == self.department.id).values(is_active=False),
                        execution_options={'synchronize_session': False})
        self.db.commit()
        with self.assertRaises(HTTPException) as caught:
            administration_lock(self.db, self.actor, include_role=True)
        self.assertEqual((caught.exception.status_code, caught.exception.detail), (403, 'Cuenta no habilitada'))

    def test_default_mode_keeps_none_and_query_without_role(self):
        self.assertIsNone(administration_lock(self.db, self.actor))
        self.assertEqual(len(self.sql), 1)
        self.assertNotIn('JOIN roles', self.sql[0])
        self.sql.clear()
        self.assertIsNone(administration_lock(self.db))
        self.assertEqual(self.sql, [])

    def test_include_role_requires_actor_without_query(self):
        with self.assertRaises(ValueError):
            administration_lock(self.db, include_role=True)
        self.assertEqual(self.sql, [])

    def test_detached_or_transient_actor_cannot_get_role(self):
        transient = User(email='other@example.invalid', nombre_completo='Ficticio', rol_id=1,
                         departamento_id=self.department.id, is_active=True)
        self.db.expunge(self.actor)
        for actor in (transient, self.actor):
            with self.subTest(actor=actor), self.assertRaises(HTTPException) as caught:
                administration_lock(self.db, actor, include_role=True)
            self.assertEqual(caught.exception.status_code, 403)
        self.assertEqual(self.sql, [])

    def test_role_is_read_after_same_shared_or_exclusive_lock(self):
        for exclusive in (False, True):
            with self.subTest(exclusive=exclusive):
                calls = []
                original_bind, original_execute = self.db.bind, self.db.execute
                fake_bind = SimpleNamespace(dialect=SimpleNamespace(name='postgresql'))
                def execute(statement):
                    self.db.bind = original_bind
                    try:
                        if isinstance(statement, TextClause):
                            calls.append(str(statement))
                            original_execute(update(User).where(User.id == self.actor.id).values(rol_id=3),
                                             execution_options={'synchronize_session': False})
                            return None
                        calls.append('REFRESH_WITH_ROLE')
                        return original_execute(statement)
                    finally:
                        self.db.bind = fake_bind
                self.db.bind, self.db.execute = fake_bind, execute
                try:
                    self.assertEqual(administration_lock(self.db, self.actor, exclusive, include_role=True), 'EMPLEADO')
                finally:
                    self.db.bind, self.db.execute = original_bind, original_execute
                function = 'pg_advisory_xact_lock' if exclusive else 'pg_advisory_xact_lock_shared'
                self.assertEqual(calls, [f'SELECT {function}(71419322)', 'REFRESH_WITH_ROLE'])


if __name__ == '__main__':
    unittest.main()
