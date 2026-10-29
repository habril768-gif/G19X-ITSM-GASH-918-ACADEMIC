"""Ciclo de Session: cierre limpio sin IO; transacciones/custom en worker protegido."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from contextvars import copy_context
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import anyio
from sqlalchemy import create_engine, event, text
from sqlalchemy.pool import StaticPool

from app.core import database


def complete(coroutine):
    """Solo dobles sin suspensión; no crea event loop ni sockets."""
    try:
        coroutine.send(None)
    except StopIteration as stopped:
        return stopped.value
    finally:
        coroutine.close()
    raise AssertionError('El doble suspendió inesperadamente')


class SessionLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://', poolclass=StaticPool,
                                    connect_args={'check_same_thread': False})
        with self.engine.begin() as connection:
            connection.execute(text('CREATE TABLE sample (value INTEGER)'))
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.calls = []
        self.scopes = []
        self.sql = []
        self.rollbacks = []
        event.listen(self.engine, 'before_cursor_execute',
                     lambda *args: self.sql.append(threading.get_ident()))
        event.listen(self.engine, 'rollback',
                     lambda *args: self.rollbacks.append(threading.get_ident()))
        scopes = self.scopes

        class Scope:
            def __init__(self, *, shield):
                self.shield = shield
            def __enter__(self):
                scopes.append(self)
            def __exit__(self, *args):
                pass

        async def run_sync(function, *, limiter):
            self.calls.append((function, limiter, bool(scopes and scopes[-1].shield)))
            return self.worker(function)

        fake = SimpleNamespace(CancelScope=Scope,
            CapacityLimiter=lambda tokens: SimpleNamespace(total_tokens=tokens),
            to_thread=SimpleNamespace(run_sync=run_sync))
        self.patches = [patch.object(database, 'get_engine', return_value=self.engine),
                        patch.object(database, 'anyio', fake)]
        for active in self.patches:
            active.start()

    def tearDown(self):
        for active in reversed(self.patches):
            active.stop()
        self.pool.shutdown()
        self.engine.dispose()

    def worker(self, function):
        return self.pool.submit(copy_context().run, function).result(timeout=5)

    def test_enter_has_no_sql_or_thread_hop_and_closes_once(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        self.assertEqual(self.sql, [])
        self.assertEqual(self.calls, [])
        with patch.object(session, 'close', wraps=session.close) as close:
            complete(dependency.aclose())
            complete(dependency.aclose())
        close.assert_called_once()
        self.assertEqual(self.calls, [])
        self.assertTrue(self.scopes[-1].shield)
        self.assertEqual(self.sql, [])
        self.assertEqual(self.rollbacks, [])

    def test_uncommitted_write_rolls_back_in_worker(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        self.worker(lambda: session.execute(text('INSERT INTO sample VALUES (1)')))
        complete(dependency.aclose())
        self.assertEqual(len(self.rollbacks), 1)
        self.assertNotEqual(self.rollbacks[0], threading.get_ident())
        with self.engine.connect() as connection:
            self.assertEqual(connection.scalar(text('SELECT count(*) FROM sample')), 0)

    def test_committed_write_is_preserved(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        def write():
            session.execute(text('INSERT INTO sample VALUES (1)'))
            session.commit()
        self.worker(write)
        self.assertFalse(session.in_transaction())
        self.sql.clear()
        complete(dependency.aclose())
        self.assertEqual(self.calls, [])
        self.assertEqual(self.sql, [])
        self.assertEqual(self.rollbacks, [])
        with self.engine.connect() as connection:
            self.assertEqual(connection.scalar(text('SELECT count(*) FROM sample')), 1)

    def test_endpoint_exception_is_preserved_and_session_closed(self):
        dependency = database.get_session()
        complete(anext(dependency))
        error = ValueError('simulado')
        with self.assertRaises(ValueError) as caught:
            complete(dependency.athrow(error))
        self.assertIs(caught.exception, error)
        self.assertEqual(self.calls, [])
        self.assertTrue(self.scopes[-1].shield)

    def test_base_exception_still_closes(self):
        dependency = database.get_session()
        complete(anext(dependency))
        error = asyncio.CancelledError()
        with self.assertRaises(asyncio.CancelledError) as caught:
            complete(dependency.athrow(error))
        self.assertIs(caught.exception, error)
        self.assertEqual(self.calls, [])
        self.assertTrue(self.scopes[-1].shield)

    def test_close_failure_propagates_without_retry(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        error = RuntimeError('cierre simulado')
        with patch.object(session, 'close', side_effect=error) as close:
            with self.assertRaises(RuntimeError) as caught:
                complete(dependency.aclose())
        self.assertIs(caught.exception, error)
        close.assert_called_once()
        self.assertEqual(self.calls, [])
        # El doble falló antes de cerrar: limpiar la sesión de prueba.
        session.close()

    def test_factory_failure_does_not_schedule_close(self):
        with patch.object(database, 'get_engine', side_effect=ValueError('configuración')):
            with self.assertRaises(ValueError):
                complete(anext(database.get_session()))
        self.assertEqual(self.calls, [])

    def test_read_transaction_rolls_back_in_shielded_independent_worker(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        self.worker(lambda: session.execute(text('SELECT 1')))
        self.sql.clear()
        complete(dependency.aclose())
        self.assertEqual(self.sql, [])
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0][1].total_tokens, 1)
        self.assertTrue(self.calls[0][2])
        self.assertEqual(len(self.rollbacks), 1)
        self.assertNotEqual(self.rollbacks[0], threading.get_ident())

    def test_read_after_commit_reopens_transaction_and_requires_worker(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        def work():
            session.execute(text('INSERT INTO sample VALUES (7)'))
            session.commit()
            session.execute(text('SELECT value FROM sample'))
        self.worker(work)
        self.assertTrue(session.in_transaction())
        complete(dependency.aclose())
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(all(ident != threading.get_ident() for ident in self.rollbacks))
        with self.engine.connect() as connection:
            self.assertEqual(connection.scalar(text('SELECT value FROM sample')), 7)

    def test_custom_session_without_transaction_keeps_worker(self):
        closed = []
        class CustomSession(database._BASE_SESSION_TYPE):
            def close(self):
                closed.append(threading.get_ident())
                super().close()
        custom = CustomSession(self.engine)
        with patch.object(database, 'Session', return_value=custom):
            dependency = database.get_session()
            complete(anext(dependency))
            complete(dependency.aclose())
        self.assertFalse(custom.in_transaction())
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(len(closed), 1)
        self.assertNotEqual(closed[0], threading.get_ident())

    def test_failed_flush_is_not_mistaken_for_transaction_free_session(self):
        from sqlalchemy import Column, Integer
        from sqlalchemy.exc import IntegrityError
        from sqlalchemy.orm import declarative_base
        Base = declarative_base()
        class Row(Base):
            __tablename__ = 'failed_flush'
            id = Column(Integer, primary_key=True)
            value = Column(Integer, unique=True)
        Base.metadata.create_all(self.engine)
        dependency = database.get_session()
        session = complete(anext(dependency))
        def fail():
            session.add_all([Row(value=1), Row(value=1)])
            session.flush()
        with self.assertRaises(IntegrityError):
            self.worker(fail)
        self.assertFalse(session.is_active)
        self.assertTrue(session.in_transaction())
        self.sql.clear()
        complete(dependency.aclose())
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.sql, [])

    def test_clean_close_detaches_expired_orm_without_sql_or_pool_activity(self):
        from sqlalchemy import Column, Integer, inspect
        from sqlalchemy.orm import declarative_base
        Base = declarative_base()
        class Row(Base):
            __tablename__ = 'clean_close'
            id = Column(Integer, primary_key=True)
        Base.metadata.create_all(self.engine)
        pool_calls = []
        def checkout(*args): pool_calls.append(('checkout', threading.get_ident()))
        def checkin(*args): pool_calls.append(('checkin', threading.get_ident()))
        event.listen(self.engine, 'checkout', checkout)
        event.listen(self.engine, 'checkin', checkin)
        try:
            dependency = database.get_session()
            session = complete(anext(dependency))
            row = Row(id=1)
            def work():
                session.add(row)
                session.commit()
            self.worker(work)
            self.assertTrue(inspect(row).expired)
            self.assertFalse(session.in_transaction())
            previous = list(pool_calls)
            self.assertEqual([kind for kind, ident in previous], ['checkout', 'checkin'])
            self.sql.clear()
            self.rollbacks.clear()
            complete(dependency.aclose())
            self.assertTrue(inspect(row).detached)
            self.assertEqual(pool_calls, previous)
            self.assertEqual(self.sql, [])
            self.assertEqual(self.rollbacks, [])
            self.assertEqual(self.calls, [])
        finally:
            event.remove(self.engine, 'checkout', checkout)
            event.remove(self.engine, 'checkin', checkin)

    def test_active_close_failure_propagates_without_retry(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        self.worker(lambda: session.execute(text('SELECT 1')))
        error = RuntimeError('cierre activo simulado')
        with patch.object(session, 'close', side_effect=error) as close:
            with self.assertRaises(RuntimeError) as caught:
                complete(dependency.aclose())
        self.assertIs(caught.exception, error)
        close.assert_called_once()
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.calls[0][2])
        self.worker(session.close)

    def test_cancellation_with_pending_write_rolls_back_in_worker(self):
        dependency = database.get_session()
        session = complete(anext(dependency))
        self.worker(lambda: session.execute(text('INSERT INTO sample VALUES (8)')))
        error = asyncio.CancelledError()
        with self.assertRaises(asyncio.CancelledError) as caught:
            complete(dependency.athrow(error))
        self.assertIs(caught.exception, error)
        self.assertEqual(len(self.calls), 1)
        self.assertTrue(self.calls[0][2])
        self.assertTrue(all(ident != threading.get_ident() for ident in self.rollbacks))
        with self.engine.connect() as connection:
            self.assertEqual(connection.scalar(text('SELECT count(*) FROM sample')), 0)


class SessionAnyIOTests(unittest.TestCase):
    """Integración AnyIO real; ejecutar también en el entorno de la autora."""
    def test_close_bypasses_saturated_default_limiter(self):
        async def scenario():
            main_thread = threading.get_ident()
            closed = []
            release = threading.Event()
            started = anyio.Event()
            limiter = anyio.to_thread.current_default_thread_limiter()
            old_tokens = limiter.total_tokens
            limiter.total_tokens = 1

            class FakeSession:
                def close(self):
                    closed.append(threading.get_ident())

            def occupy():
                anyio.from_thread.run_sync(started.set)
                if not release.wait(timeout=5):
                    raise AssertionError('No se liberó el worker de prueba')

            try:
                with patch.object(database, 'get_engine', return_value=object()), \
                     patch.object(database, 'Session', return_value=FakeSession()):
                    async with anyio.create_task_group() as group:
                        group.start_soon(anyio.to_thread.run_sync, occupy)
                        await started.wait()
                        try:
                            with anyio.fail_after(2):
                                dependency = database.get_session()
                                await anext(dependency)
                                await dependency.aclose()
                            self.assertEqual(len(closed), 1)
                            self.assertNotEqual(closed[0], main_thread)
                        finally:
                            release.set()
            finally:
                release.set()
                limiter.total_tokens = old_tokens
        anyio.run(scenario)

    def test_cancelled_scope_closes_before_cancellation_propagates(self):
        async def scenario():
            main_thread = threading.get_ident()
            closed = []
            observed = []

            class FakeSession:
                def close(self):
                    closed.append(threading.get_ident())

            with patch.object(database, 'get_engine', return_value=object()), \
                 patch.object(database, 'Session', return_value=FakeSession()):
                with anyio.CancelScope() as scope:
                    try:
                        async with asynccontextmanager(database.get_session)():
                            scope.cancel()
                            await anyio.sleep(0)
                    except anyio.get_cancelled_exc_class():
                        observed.append(len(closed))
                        raise
            self.assertEqual(observed, [1])
            self.assertEqual(len(closed), 1)
            self.assertNotEqual(closed[0], main_thread)
        anyio.run(scenario)


class SessionFastAPITests(unittest.TestCase):
    def test_real_dependency_rolls_back_after_success_and_http_error(self):
        from fastapi import Depends, FastAPI, HTTPException
        from fastapi.testclient import TestClient
        from sqlalchemy.orm import Session

        engine = create_engine('sqlite://', poolclass=StaticPool,
                               connect_args={'check_same_thread': False})
        with engine.begin() as connection:
            connection.execute(text('CREATE TABLE sample (value INTEGER)'))
        closed = []
        served = []
        created = []
        class ObservedSession(Session):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                created.append(threading.get_ident())
            def close(self):
                closed.append(threading.get_ident())
                super().close()

        app = FastAPI()
        @app.post('/sample/{failure}')
        def write(failure: bool, session=Depends(database.get_session)):
            served.append(threading.get_ident())
            session.execute(text('INSERT INTO sample VALUES (1)'))
            if failure:
                raise HTTPException(status_code=409, detail='simulado')
            return {'ok': True}

        try:
            with patch.object(database, 'get_engine', return_value=engine), \
                 patch.object(database, 'Session', ObservedSession):
                with TestClient(app) as client:
                    for failure, expected in [('false', 200), ('true', 409)]:
                        response = client.post('/sample/' + failure)
                        self.assertEqual(response.status_code, expected)
                        with engine.connect() as connection:
                            self.assertEqual(connection.scalar(text('SELECT count(*) FROM sample')), 0)
            self.assertEqual(len(closed), 2)
            self.assertEqual(len(created), 2)
            for loop_thread, endpoint_thread, close_thread in zip(created, served, closed):
                self.assertNotEqual(loop_thread, endpoint_thread)
                self.assertNotEqual(loop_thread, close_thread)
        finally:
            engine.dispose()


    def test_committed_standard_session_closes_on_loop_without_io(self):
        from fastapi import Depends, FastAPI
        from fastapi.testclient import TestClient
        engine = create_engine('sqlite://', poolclass=StaticPool,
                               connect_args={'check_same_thread': False})
        with engine.begin() as connection:
            connection.execute(text('CREATE TABLE committed_sample (value INTEGER)'))
        original_close = database._BASE_SESSION_TYPE.close
        closed, sql_threads, loop_threads, worker_threads = [], [], [], []
        def observe(conn, cursor, statement, parameters, context, executemany):
            sql_threads.append(threading.get_ident())
        def close(session):
            before = len(sql_threads)
            self.assertFalse(session.in_transaction())
            original_close(session)
            closed.append((threading.get_ident(), len(sql_threads)-before))
        event.listen(engine, 'before_cursor_execute', observe)
        app = FastAPI()
        @app.middleware('http')
        async def record_loop(request, call_next):
            loop_threads.append(threading.get_ident())
            return await call_next(request)
        @app.post('/committed')
        def write(session=Depends(database.get_session)):
            worker_threads.append(threading.get_ident())
            session.execute(text('INSERT INTO committed_sample VALUES (1)'))
            session.commit()
            return {'ok': True}
        try:
            with patch.object(database, 'get_engine', return_value=engine), \
                 patch.object(database._BASE_SESSION_TYPE, 'close', close):
                with TestClient(app) as client:
                    response = client.post('/committed')
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json(), {'ok': True})
            self.assertEqual(len(closed), 1)
            self.assertEqual(closed[0], (loop_threads[0], 0))
            self.assertNotEqual(worker_threads[0], loop_threads[0])
            self.assertEqual(sql_threads, worker_threads)
            with engine.connect() as connection:
                self.assertEqual(connection.scalar(text('SELECT count(*) FROM committed_sample')), 1)
        finally:
            event.remove(engine, 'before_cursor_execute', observe)
            engine.dispose()


if __name__ == '__main__':
    unittest.main()
