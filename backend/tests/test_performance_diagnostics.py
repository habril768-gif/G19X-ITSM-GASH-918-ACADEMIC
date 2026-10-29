"""Diagnóstico QA: pruebas sin Docker, proveedores ni dependencias web."""
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from uuid import UUID

backend = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("qa_timing", backend / "app/core/performance_timing.py")
timing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(timing)
sys.path.insert(0, str(backend / "scripts"))
import provision_performance_qa as provision
import performance_runner as runner
import performance_host as host


def run_async(coroutine):
    # Estas dobles ASGI no suspenden: ejecutar sin loop evita abrir sockets locales.
    try:
        coroutine.send(None)
    except StopIteration as done:
        return done.value
    finally:
        coroutine.close()
    raise AssertionError("La doble ASGI suspendió inesperadamente")


def attach_thread_fixture(groups):
    for group in groups.values():
        n=group['solicitudes']
        for field in ('thread_calls','thread_wait','thread_run','thread_resume'):
            group['metricas'][field]={'media':1}
        group['metricas']['thread_incomplete']={'media':0}
        group['thread_stages']={'other':{'calls':n,'wait_ms':n,'run_ms':n,'resume_ms':n,'incomplete':0}}


class DiagnosticTests(unittest.TestCase):
    def test_guard_rejects_operational_database_and_providers(self):
        env = dict(QA_PERF_DIAGNOSTIC_RUN_ID="qa123456", POSTGRES_DB="plurione_test_perf_qa123456",
            POSTGRES_USER="qa_perf_qa123456", POSTGRES_HOST="postgres", AI_ENABLED="false", MAIL_ENABLED="false")
        timing.guard(env)
        for key, value in (("POSTGRES_DB", "plurione"), ("POSTGRES_USER", "plurione"),
                ("POSTGRES_HOST", "localhost"), ("AI_ENABLED", "true"), ("MAIL_ENABLED", "true"),
                ("QA_PERF_DIAGNOSTIC_RUN_ID", "invalid/../")):
            with self.assertRaisesRegex(RuntimeError, "FUERA_DE_QA"):
                timing.guard(dict(env, **{key: value}))

    def test_routes_are_reduced_to_fixed_labels(self):
        cid = str(UUID(int=1))
        self.assertEqual(timing.operation("GET", "/incidents/" + cid), "detalle")
        self.assertEqual(timing.operation("PUT", "/incidents/" + cid + "/content"), "actualizacion")
        for path in ("/auth/login", "/incidents/options", "/incidents/invalid", "/incidents/" + cid + "/history"):
            self.assertIsNone(timing.operation("GET", path))

    def test_asgi_aggregation_and_thread_context_do_not_save_private_values(self):
        async def scenario():
            def sync_work():
                state = timing.current.get()
                timing.add_sql(state, "SELECT/users", .1)
                state["consultas"] += 1
                return "PRIVATE_CASE_BODY"
            endpoint = timing.timed("endpoint", sync_work)
            auth = timing.timed("auth", lambda: True)
            async def app(scope, receive, send):
                with ThreadPoolExecutor(max_workers=1) as pool:
                    pool.submit(copy_context().run, auth).result()
                    pool.submit(copy_context().run, endpoint).result()
                await send({"type": "http.response.start", "status": 200})
                await send({"type": "http.response.body", "body": b"PRIVATE_CASE_BODY"})
            wrapped = timing.Timing(app)
            async def send(message): pass
            scope = {"type": "http", "method": "GET", "path": "/incidents/" + str(UUID(int=1)),
                "headers": [(b"x-qa-performance-phase", b"medicion"), (b"authorization", b"Bearer PRIVATE_TOKEN")]}
            with ThreadPoolExecutor(max_workers=5) as pool:
                futures = [pool.submit(lambda: run_async(wrapped(scope, None, send))) for _ in range(5)]
                for future in futures:
                    future.result()
            self.assertIsNone(timing.current.get())
            snapshot = wrapped.snapshot()
            group = snapshot["grupos"]["medicion/detalle"]
            self.assertEqual(group["solicitudes"], 5)
            self.assertEqual(group["metricas"]["consultas"]["media"], 1)
            self.assertGreater(group["metricas"]["auth"]["media"], 0)
            self.assertGreater(group["metricas"]["endpoint"]["media"], 0)
            self.assertNotIn("PRIVATE", json.dumps(snapshot))
            self.assertNotIn(str(UUID(int=1)), json.dumps(snapshot))
        run_async(scenario())

    def test_missing_phase_header_does_not_collect_preflight(self):
        async def app(scope, receive, send): pass
        wrapper = timing.Timing(app)
        run_async(wrapper({"type": "http", "method": "GET", "path": "/incidents", "headers": []}, None, None))
        self.assertEqual(wrapper.snapshot()["grupos"], {})

    def test_failures_are_counted_and_context_is_reset(self):
        async def app(scope, receive, send): raise ValueError("private error")
        wrapper = timing.Timing(app)
        with self.assertRaises(ValueError):
            run_async(wrapper({"type": "http", "method": "POST", "path": "/incidents",
                "headers": [(b"x-qa-performance-phase", b"medicion")]}, None, None))
        self.assertIsNone(timing.current.get())
        self.assertEqual(wrapper.snapshot()["grupos"]["medicion/creacion"]["errores"], 1)
        self.assertNotIn("private error", json.dumps(wrapper.snapshot()))

    def test_shutdown_prints_only_aggregate_marker(self):
        async def app(scope, receive, send):
            await send({"type": "lifespan.shutdown.complete"})
        async def send(message): pass
        with contextlib.redirect_stdout(io.StringIO()) as output:
            run_async(timing.Timing(app)({"type": "lifespan"}, None, send))
        self.assertTrue(output.getvalue().startswith(timing.MARKER))
        self.assertEqual(json.loads(output.getvalue()[len(timing.MARKER):])["version"], 5)

    def test_ordinary_specification_has_no_diagnostic_entry(self):
        normal = provision.specification(Path.cwd(), "qa123456", 18080)
        self.assertNotIn("command", normal["services"]["api"])
        self.assertNotIn("QA_PERF_DIAGNOSTIC_RUN_ID", normal["services"]["api"]["environment"])
        diagnostic = provision.specification(Path.cwd(), "qa123456", 18080, True)
        self.assertIn("app.core.performance_diagnostics:app", diagnostic["services"]["api"]["command"])

    def test_diagnostic_full_is_rejected_before_creating_files(self):
        with self.assertRaisesRegex(provision.ProvisionError, "SOLO_SMOKE"):
            provision.run(Path.cwd(), "full", "docker", diagnostic=True)

    def test_missing_or_mismatched_shutdown_data_is_rejected(self):
        groups, measured = {}, {}
        for phase in ("calentamiento", "medicion"):
            measured[phase] = {"metricas": {}}
            for op in runner.OPS:
                measured[phase]["metricas"][op] = {"intentos": 2}
                groups[phase + "/" + op] = {"solicitudes": 2, "errores": 0,
                    "metricas": {field: {"media": 1} for field in ("total", "auth", "endpoint", "sql", "consultas")},
                    "familias_sql": {"SELECT/users": {"consultas": 2, "ms": 2}}}
        attach_thread_fixture(groups)
        value = {"version": 3, "limite_excedido": False, "grupos": groups}
        line = timing.MARKER + json.dumps(value)
        self.assertEqual(provision.read_diagnostics(line, measured), value)
        for invalid in ("", line + "\n" + line, timing.MARKER + json.dumps(dict(value, limite_excedido=True))):
            with self.assertRaises(provision.ProvisionError):
                provision.read_diagnostics(invalid, measured)
        groups["medicion/listado"]["solicitudes"] = 1
        with self.assertRaisesRegex(provision.ProvisionError, "CONTEO"):
            provision.read_diagnostics(timing.MARKER + json.dumps(value), measured)

    def test_phase_headers_are_opt_in_and_never_added_to_login(self):
        client = runner.Client(18080)
        fake_response = type("Response", (), {"status": 200, "read": lambda self, size: b"{}"})()
        from unittest.mock import Mock
        conn = Mock()
        conn.getresponse.return_value = fake_response
        client.connection = conn
        client.phase = "medicion"
        client.request("GET", "/incidents")
        self.assertNotIn("X-QA-Performance-Phase", conn.request.call_args.kwargs["headers"])
        client.diagnostic = True
        client.request("GET", "/incidents")
        self.assertEqual(conn.request.call_args.kwargs["headers"]["X-QA-Performance-Phase"], "medicion")
        client.phase = None
        client.request("POST", "/auth/login")
        self.assertNotIn("X-QA-Performance-Phase", conn.request.call_args.kwargs["headers"])


    def test_sql_families_are_fixed_labels_without_literals(self):
        self.assertEqual(timing.sql_family('SELECT users.id FROM users JOIN departamentos ON users.departamento_id = departamentos.id WHERE users.email = :private'), 'SELECT/departamentos+users')
        self.assertEqual(timing.sql_family('INSERT INTO mail_deliveries VALUES (:private)'), 'INSERT/mail_deliveries')
        self.assertEqual(timing.sql_family('UPDATE incidencias SET titulo=:private'), 'UPDATE/incidencias')
        self.assertEqual(timing.sql_family('SELECT pg_advisory_xact_lock_shared(71419322)'), 'SELECT/advisory_lock')
        self.assertEqual(timing.sql_family('SELECT * FROM "auth_sessions"'), 'SELECT/auth_sessions')
        self.assertEqual(timing.sql_family('SELECT private_literal FROM unknown_private_table'), 'SELECT/otras')
        self.assertNotIn('private', timing.sql_family('DELETE FROM unknown_private_table WHERE secret=1'))

    def test_family_totals_sum_across_requests_with_missing_families(self):
        rows = [{"familias_sql": {"SELECT/users": {"consultas": 2, "ms": 4},
                                 "INSERT/incidencias": {"consultas": 1, "ms": 3}}},
                {"familias_sql": {"SELECT/users": {"consultas": 1, "ms": 2}}}]
        result = timing.family_summary(rows)
        self.assertEqual(result['SELECT/users']['consultas'], 3)
        self.assertEqual(result['SELECT/users']['ms_por_peticion'], 3)
        self.assertEqual(result['INSERT/incidencias']['consultas_por_peticion'], .5)

    def test_response_body_and_cleanup_are_separated(self):
        ticks = iter([0.0, .010, .040])
        async def app(scope, receive, send):
            await send({"type": "http.response.start", "status": 200})
            await send({"type": "http.response.body", "body": b"{}"})
        async def send(message): pass
        wrapper = timing.Timing(app)
        with patch.object(timing.time, 'perf_counter', side_effect=lambda: next(ticks)):
            run_async(wrapper({"type": "http", "method": "GET", "path": "/incidents",
                "headers": [(b"x-qa-performance-phase", b"medicion")]}, None, send))
        metrics = wrapper.snapshot()['grupos']['medicion/listado']['metricas']
        self.assertEqual(metrics['hasta_envio']['media'], 10)
        self.assertEqual(metrics['cierre']['media'], 30)
        self.assertEqual(metrics['total']['media'], 40)

    def test_cpu_percentages_distinguish_core_and_machine(self):
        with patch.object(host.os, 'cpu_count', return_value=4):
            result = host.summarize({'wall': 0, 'process': 4, 'host': (100, 200)},
                                    {'wall': 10, 'process': 9, 'host': (150, 400)})
        self.assertEqual(result['generador_cpu_porcentaje_un_nucleo'], 50)
        self.assertEqual(result['generador_cpu_porcentaje_equipo'], 12.5)
        self.assertEqual(result['host_cpu_porcentaje'], 75)
        self.assertEqual(result['host_estado'], 'OK')

    def test_missing_cpu_is_unavailable_not_zero(self):
        result = host.summarize({'wall': 0, 'process': 0, 'host': None},
                                {'wall': 1, 'process': 0, 'host': None})
        self.assertIsNone(result['host_cpu_porcentaje'])
        self.assertEqual(result['host_estado'], 'NO_DISPONIBLE')
        self.assertEqual(host.summarize({'wall': 1}, {'wall': 1})['estado'], 'INTERVALO_INVALIDO')

    def test_inconsistent_family_counts_or_times_are_rejected(self):
        measured, groups = {}, {}
        for phase in ('calentamiento', 'medicion'):
            measured[phase] = {'metricas': {}}
            for op in runner.OPS:
                measured[phase]['metricas'][op] = {'intentos': 1}
                groups[phase + '/' + op] = {'solicitudes': 1, 'errores': 0,
                    'metricas': {field: {'media': 1} for field in ('total', 'auth', 'endpoint', 'sql', 'consultas')},
                    'familias_sql': {'SELECT/users': {'consultas': 1, 'ms': 1}}}
        attach_thread_fixture(groups)
        value = {'version': 3, 'limite_excedido': False, 'grupos': groups}
        for change in ({'consultas': 2, 'ms': 1}, {'consultas': 1, 'ms': 2}):
            groups['medicion/listado']['familias_sql']['SELECT/users'] = change
            with self.assertRaises(provision.ProvisionError):
                provision.read_diagnostics(timing.MARKER + json.dumps(value), measured)



    def test_baseline_weights_valid_intervals_and_preserves_unavailable(self):
        stamps = [{"i": i} for i in range(4)]
        rows = [{"duracion_s": 2, "host_estado": "OK", "host_cpu_porcentaje": 20},
                {"duracion_s": 4, "host_estado": "OK", "host_cpu_porcentaje": 50},
                {"duracion_s": 2, "host_estado": "NO_DISPONIBLE", "host_cpu_porcentaje": None}]
        with patch.object(host, 'stamp', side_effect=stamps), patch.object(host, 'summarize', side_effect=rows), patch.object(host.time, 'sleep') as sleep:
            result = host.baseline()
        self.assertEqual(sleep.call_count, 3)
        self.assertEqual(result['intervalos_validos'], 2)
        self.assertEqual(result['media_cpu_global_porcentaje'], 40)
        self.assertIsNone(result['intervalos'][2]['cpu_global_porcentaje'])

    def test_baseline_does_not_report_zero_when_all_samples_unavailable(self):
        with patch.object(host, 'stamp', return_value={}), patch.object(host, 'summarize', return_value={
                'duracion_s': 2, 'host_estado': 'NO_DISPONIBLE', 'host_cpu_porcentaje': None}), patch.object(host.time, 'sleep'):
            result = host.baseline()
        self.assertEqual(result['intervalos_validos'], 0)
        self.assertIsNone(result['media_cpu_global_porcentaje'])



    def test_threadpool_wait_execution_and_resume_preserve_options(self):
        state=dict.fromkeys(timing.FIELDS,0.0);state['thread_stages']={}
        calls=[]
        async def original(fn,*args,**kwargs):
            calls.append((args,kwargs));return fn(*args)
        def current_user(value):return value+1
        observed=timing.instrument_threadpool(original)
        token=timing.current.set(state)
        limiter=object()
        try:
            with patch.object(timing.time,'perf_counter',side_effect=[0,.010,.030,.040]):
                result=run_async(observed(current_user,7,limiter=limiter,abandon_on_cancel=True))
        finally:timing.current.reset(token)
        self.assertEqual(result,8)
        self.assertEqual(calls,[((7,),{'limiter':limiter,'abandon_on_cancel':True})])
        self.assertAlmostEqual(state['thread_wait'],10)
        self.assertAlmostEqual(state['thread_run'],20)
        self.assertAlmostEqual(state['thread_resume'],10)
        self.assertEqual(state['thread_calls'],1)
        self.assertEqual(state['thread_incomplete'],0)
        self.assertEqual(set(state['thread_stages']),{'auth'})

    def test_threadpool_outside_request_passes_original_callable(self):
        calls=[]
        async def original(fn,*args,**kwargs):calls.append((fn,args,kwargs));return fn(*args)
        def fn(value):return value
        self.assertEqual(run_async(timing.instrument_threadpool(original)(fn,3,cancellable=False)),3)
        self.assertIs(calls[0][0],fn)
        self.assertEqual(calls[0][2],{'cancellable':False})

    def test_threadpool_preserves_exception_without_recording_message(self):
        state=dict.fromkeys(timing.FIELDS,0.0);state['thread_stages']={}
        error=ValueError('PRIVATE_ERROR_DATA')
        def broken():raise error
        async def original(fn,*args,**kwargs):return fn(*args)
        token=timing.current.set(state)
        try:
            with self.assertRaises(ValueError) as caught:
                run_async(timing.instrument_threadpool(original)(broken))
        finally:timing.current.reset(token)
        self.assertIs(caught.exception,error)
        self.assertEqual(state['thread_calls'],1)
        self.assertEqual(state['thread_incomplete'],0)
        self.assertNotIn('PRIVATE',json.dumps(timing.thread_summary([state])))

    def test_unstarted_thread_is_marked_incomplete(self):
        state=dict.fromkeys(timing.FIELDS,0.0);state['thread_stages']={}
        async def original(fn,*args,**kwargs):raise RuntimeError('not started')
        token=timing.current.set(state)
        try:
            with self.assertRaises(RuntimeError):
                run_async(timing.instrument_threadpool(original)(lambda:None))
        finally:timing.current.reset(token)
        self.assertEqual(state['thread_incomplete'],1)
        self.assertEqual(state['thread_calls'],1)

    def test_thread_categories_are_fixed_and_unwrap_partial(self):
        from functools import partial
        def _run_sync_endpoint():pass
        def validate():pass
        validate.__module__='fastapi._compat.v2'
        class Manager:
            def __enter__(self):return self
            def __exit__(self,*args):return None
        def PRIVATE_FUNCTION():pass
        self.assertEqual(timing.thread_stage(partial(_run_sync_endpoint)), 'endpoint')
        self.assertEqual(timing.thread_stage(validate),'response_validation')
        self.assertEqual(timing.thread_stage(Manager().__enter__),'dependency_enter')
        self.assertEqual(timing.thread_stage(Manager().__exit__),'dependency_exit')
        self.assertEqual(timing.thread_stage(PRIVATE_FUNCTION),'other')

    def test_thread_wrapper_with_real_worker_preserves_context(self):
        state=dict.fromkeys(timing.FIELDS,0.0);state['thread_stages']={}
        async def original(fn,*args,**kwargs):
            with ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(copy_context().run,fn,*args).result()
        def work(value):
            self.assertIs(timing.current.get(),state)
            return value*2
        token=timing.current.set(state)
        try:result=run_async(timing.instrument_threadpool(original)(work,4))
        finally:timing.current.reset(token)
        self.assertEqual(result,8)
        self.assertEqual(state['thread_calls'],1)
        self.assertEqual(state['thread_incomplete'],0)

    def test_thread_stage_summary_averages_over_requests(self):
        rows=[{'thread_stages':{'auth':{'calls':2,'wait_ms':4,'run_ms':8,'resume_ms':2,'incomplete':0}}},
              {'thread_stages':{'auth':{'calls':1,'wait_ms':2,'run_ms':4,'resume_ms':1,'incomplete':0}}}]
        result=timing.thread_summary(rows)['auth']
        self.assertEqual(result['calls'],3)
        self.assertEqual(result['calls_per_request'],1.5)
        self.assertEqual(result['wait_ms_per_request'],3)
        self.assertEqual(result['run_ms_per_request'],6)

    def test_inconsistent_thread_totals_and_incomplete_are_rejected(self):
        measured,groups={},{}
        for phase in ('calentamiento','medicion'):
            measured[phase]={'metricas':{}}
            for op in runner.OPS:
                measured[phase]['metricas'][op]={'intentos':1}
                groups[phase+'/'+op]={'solicitudes':1,'errores':0,
                    'metricas':{field:{'media':1} for field in ('total','auth','endpoint','sql','consultas')},
                    'familias_sql':{'SELECT/users':{'consultas':1,'ms':1}}}
        attach_thread_fixture(groups)
        value={'version':3,'limite_excedido':False,'grupos':groups}
        groups['medicion/listado']['thread_stages']['other']['wait_ms']=99
        with self.assertRaisesRegex(provision.ProvisionError,'HILOS_SUMAS'):
            provision.read_diagnostics(timing.MARKER+json.dumps(value),measured)
        groups['medicion/listado']['thread_stages']['other']['wait_ms']=1
        groups['medicion/listado']['metricas']['thread_incomplete']['media']=1
        with self.assertRaisesRegex(provision.ProvisionError,'HILOS_INCOMPLETOS'):
            provision.read_diagnostics(timing.MARKER+json.dumps(value),measured)



class PreparedWorkerClassificationTests(unittest.TestCase):
    def test_known_prepared_worker_is_endpoint_but_other_modules_are_not(self):
        def _run_validated_endpoint(): pass
        _run_validated_endpoint.__module__ = 'app.core.worker_response'
        self.assertEqual(timing.thread_stage(_run_validated_endpoint), 'endpoint')
        _run_validated_endpoint.__module__ = 'unrelated'
        self.assertEqual(timing.thread_stage(_run_validated_endpoint), 'other')


if __name__ == "__main__": unittest.main()
