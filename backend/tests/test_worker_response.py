"""DTO en worker: accesos ORM, errores, firma e integración FastAPI."""
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from functools import partial
import inspect
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import BaseModel, ConfigDict
from sqlalchemy.exc import SQLAlchemyError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core import worker_response as execution
from app.core import performance_timing as timing


class DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    value: int


def complete(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as stopped:
        return stopped.value
    finally:
        coroutine.close()
    raise AssertionError('El doble suspendió inesperadamente')


class WorkerResponseTests(unittest.TestCase):
    def setUp(self):
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.addCleanup(self.pool.shutdown)
        self.calls = []
        async def offload(function, *args, **kwargs):
            self.calls.append(function)
            return self.pool.submit(copy_context().run, partial(function, *args, **kwargs)).result(timeout=5)
        active = patch.object(execution, 'run_in_threadpool', offload)
        active.start()
        self.addCleanup(active.stop)

    def test_attribute_reads_and_validation_finish_inside_single_worker(self):
        owner = threading.get_ident()
        reads = []
        class Row:
            @property
            def value(self):
                if threading.get_ident() == owner:
                    raise AssertionError('Acceso ORM en hilo principal')
                reads.append(threading.get_ident())
                return 7
        def source():
            return Row()
        endpoint = execution.worker_response(DTO)(source)
        result = complete(endpoint())
        self.assertIsInstance(result, DTO)
        self.assertEqual(result.model_dump(), {'value': 7})
        self.assertEqual(len(reads), 1)
        self.assertEqual(len(self.calls), 1)

    def test_invalid_response_uses_fastapi_error_with_response_location(self):
        endpoint = execution.worker_response(DTO)(lambda: {'value': 'inválido'})
        with self.assertRaises(ResponseValidationError) as caught:
            complete(endpoint())
        self.assertEqual(caught.exception.errors()[0]['loc'], ('response', 'value'))
        self.assertEqual(caught.exception.body, {'value': 'inválido'})

    def test_http_exception_is_propagated_unchanged(self):
        error = HTTPException(403, 'Simulado')
        def source():
            raise error
        with self.assertRaises(HTTPException) as caught:
            complete(execution.worker_response(DTO)(source)())
        self.assertIs(caught.exception, error)
        self.assertEqual(len(self.calls), 1)

    def test_commit_exception_cannot_produce_success_dto(self):
        error = SQLAlchemyError('Commit simulado')
        def source():
            raise error
        with self.assertRaises(SQLAlchemyError) as caught:
            complete(execution.worker_response(DTO)(source)())
        self.assertIs(caught.exception, error)

    def test_signature_annotations_and_async_route_are_preserved(self):
        def source(value: int, *, extra: int = 2):
            return {'value': value + extra}
        endpoint = execution.worker_response(DTO)(source)
        self.assertTrue(inspect.iscoroutinefunction(endpoint))
        self.assertEqual(inspect.signature(endpoint), inspect.signature(source))
        self.assertEqual(complete(endpoint(3, extra=4)).value, 7)

    def test_qa_binds_timed_worker_without_sync_route_or_extra_call(self):
        def source():
            return {'value': 4}
        endpoint = execution.worker_response(DTO)(source)
        observed = endpoint.with_response_worker(timing.timed('endpoint', endpoint.response_worker))
        self.assertTrue(inspect.iscoroutinefunction(observed))
        self.assertEqual(timing.thread_stage(observed.response_worker), 'endpoint')
        state = dict.fromkeys(timing.FIELDS, 0.0)
        token = timing.current.set(state)
        try:
            self.assertEqual(complete(observed()).value, 4)
        finally:
            timing.current.reset(token)
        self.assertGreater(state['endpoint'], 0)
        self.assertEqual(len(self.calls), 1)

    def test_calls_return_independent_dtos(self):
        def source(value):
            return {'value': value}
        endpoint = execution.worker_response(DTO)(source)
        first, second = complete(endpoint(1)), complete(endpoint(2))
        self.assertIsNot(first, second)
        self.assertEqual((first.value, second.value), (1, 2))


class WorkerResponseFastAPITests(unittest.TestCase):
    def test_real_fastapi_has_one_worker_call_and_no_threaded_response_validation(self):
        import anyio.to_thread
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        app = FastAPI()
        source_threads = []
        @app.get('/sample', response_model=DTO)
        @execution.worker_response(DTO)
        def source(value: int):
            source_threads.append(threading.get_ident())
            return {'value': value}
        calls = []
        original = anyio.to_thread.run_sync
        async def spy(function, *args, **kwargs):
            calls.append(timing.thread_stage(function))
            return await original(function, *args, **kwargs)
        with TestClient(app) as client:
            with patch.object(anyio.to_thread, 'run_sync', spy):
                response = client.get('/sample?value=7')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'value': 7})
        self.assertEqual(calls, ['endpoint'])
        self.assertEqual(len(source_threads), 1)

    def test_real_fastapi_invalid_output_still_returns_server_error(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        app = FastAPI()
        @app.get('/sample', response_model=DTO)
        @execution.worker_response(DTO)
        def source():
            return {'value': 'inválido'}
        with TestClient(app, raise_server_exceptions=False) as client:
            self.assertEqual(client.get('/sample').status_code, 500)


if __name__ == '__main__':
    unittest.main()
