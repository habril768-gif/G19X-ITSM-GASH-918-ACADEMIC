"""Ping QA: medicion sin datos privados y lectura compatible v3/v4, sin SQLAlchemy."""
import copy
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

backend=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qa_pool_timing',backend/'app/core/performance_timing.py')
timing=importlib.util.module_from_spec(spec);spec.loader.exec_module(timing)
sys.path.insert(0,str(backend/'scripts'))
import provision_performance_qa as provision
import performance_runner as runner


def state():return dict.fromkeys(timing.FIELDS,0.0)


def fixture(version=4):
    groups,measured={},{}
    for phase in ('calentamiento','medicion'):
        measured[phase]={'metricas':{}}
        for op in runner.OPS:
            measured[phase]['metricas'][op]={'intentos':2}
            metrics={f:{'media':1} for f in ('total','auth','endpoint','sql','consultas','thread_calls','thread_wait','thread_run','thread_resume')}
            metrics['thread_incomplete']={'media':0}
            if version==4:
                metrics.update(pool_ping={'media':2,'p95':3,'max':3},
                    pool_ping_calls={'media':.5,'p95':1,'max':1},pool_ping_errors={'media':0,'p95':0,'max':0})
            groups[phase+'/'+op]={'solicitudes':2,'errores':0,'metricas':metrics,
                'familias_sql':{'SELECT/users':{'consultas':2,'ms':2}},
                'thread_stages':{'other':{'calls':2,'wait_ms':2,'run_ms':2,'resume_ms':2,'incomplete':0}}}
    result={'version':version,'limite_excedido':False,'grupos':groups}
    if version==4:result['pool_ping_instrumentado']=True
    return result,measured


class PoolPingTests(unittest.TestCase):
    def test_result_arguments_and_elapsed_preserved(self):
        row=state();calls=[];connection=object()
        def original(*args,**kwargs):calls.append((args,kwargs));return True
        token=timing.current.set(row)
        try:
            with patch.object(timing.time,'perf_counter',side_effect=[1,1.012]):
                self.assertIs(timing.instrument_pool_ping(original)(connection,option=True),True)
        finally:timing.current.reset(token)
        self.assertEqual(calls,[((connection,),{'option':True})])
        self.assertAlmostEqual(row['pool_ping'],12)
        self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,0))
        self.assertEqual(row['sql'],0);self.assertEqual(row['consultas'],0)

    def test_outside_request_does_not_time_or_change_result(self):
        sentinel=object()
        with patch.object(timing.time,'perf_counter',side_effect=AssertionError('No cronometrar')):
            self.assertIs(timing.instrument_pool_ping(lambda value:value)(sentinel),sentinel)
        self.assertIsNone(timing.current.get())

    def test_false_result_counted_without_retry(self):
        row=state();calls=[];token=timing.current.set(row)
        try:
            def original():calls.append(True);return False
            self.assertIs(timing.instrument_pool_ping(original)(),False)
        finally:timing.current.reset(token)
        self.assertEqual(len(calls),1)
        self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,1))

    def test_exception_identity_preserved_without_private_data(self):
        class Cancelled(BaseException):pass
        for error in (ValueError('PRIVATE_PASSWORD'),Cancelled('PRIVATE_TOKEN')):
            row=state();calls=[];token=timing.current.set(row)
            try:
                def original(*args):calls.append(True);raise error
                with self.assertRaises(type(error)) as caught:
                    timing.instrument_pool_ping(original)('PRIVATE_CONNECTION')
            finally:timing.current.reset(token)
            self.assertIs(caught.exception,error)
            self.assertEqual(len(calls),1)
            self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,1))
            self.assertNotIn('PRIVATE',json.dumps(row))

    def test_concurrent_contexts_do_not_share_counters(self):
        observed=timing.instrument_pool_ping(lambda:True)
        def work(count):
            row=state();token=timing.current.set(row)
            try:
                for _ in range(count):observed()
            finally:timing.current.reset(token)
            return row
        with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(work,range(1,9)))
        self.assertEqual([row['pool_ping_calls'] for row in rows],list(range(1,9)))
        self.assertIsNone(timing.current.get())

    def test_v3_remains_readable_and_v4_requires_pool_metrics(self):
        for version in (3,4):
            data,measured=fixture(version)
            self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(data),measured),data)
        data,measured=fixture(4)
        for mutate in (lambda x:x.pop('pool_ping_instrumentado'),
                       lambda x:x['grupos']['medicion/listado']['metricas'].pop('pool_ping')):
            invalid=copy.deepcopy(data);mutate(invalid)
            with self.assertRaises(provision.ProvisionError):provision.read_diagnostics(timing.MARKER+json.dumps(invalid),measured)

    def test_invalid_pool_metrics_are_rejected(self):
        data,measured=fixture(4)
        changes=[('pool_ping',{'media':float('nan'),'p95':3,'max':3}),
                 ('pool_ping',{'media':-1,'p95':3,'max':3}),
                 ('pool_ping',{'media':'PRIVATE','p95':3,'max':3}),
                 ('pool_ping',{'media':True,'p95':3,'max':3}),
                 ('pool_ping',{'media':2,'p95':float('inf'),'max':3}),
                 ('pool_ping',{'media':4,'p95':3,'max':3}),
                 ('pool_ping_calls',{'media':.1,'p95':1,'max':1}),
                 ('pool_ping_calls',{'media':0,'p95':0,'max':0}),
                 ('pool_ping_errors',{'media':1,'p95':1,'max':1})]
        for field,stats in changes:
            invalid=copy.deepcopy(data);invalid['grupos']['medicion/listado']['metricas'][field]=stats
            with self.subTest(field=field,stats=stats),self.assertRaises(provision.ProvisionError):
                provision.read_diagnostics(timing.MARKER+json.dumps(invalid),measured)

    def test_zero_pings_allowed_for_fresh_connection(self):
        data,measured=fixture(4)
        for group in data['grupos'].values():
            for field in ('pool_ping','pool_ping_calls','pool_ping_errors'):
                group['metricas'][field]={'media':0,'p95':0,'max':0}
        self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(data),measured),data)

    def test_current_asgi_snapshot_with_ping_passes_full_report_reader(self):
        async def original_worker(fn, *args, **kwargs): return fn(*args)
        worker=timing.instrument_threadpool(original_worker)
        ping=timing.instrument_pool_ping(lambda connection: True)
        auth=timing.timed('auth',lambda: True)
        def query():
            ping(object())
            row=timing.current.get()
            row['consultas']+=1
            timing.add_sql(row,'SELECT/users',.001)
        endpoint=timing.timed('endpoint',query)
        async def app(scope,receive,send):
            await worker(auth)
            await worker(endpoint)
            await send({'type':'http.response.start','status':201 if scope['method']=='POST' else 200})
            await send({'type':'http.response.body','body':b'{}'})
        async def send(message):pass
        def complete(coroutine):
            try:coroutine.send(None)
            except StopIteration as done:return done.value
            finally:coroutine.close()
            raise AssertionError('Doble suspendida')
        wrapper=timing.Timing(app,pool_ping_instrumented=True,thread_cpu_instrumented=True)
        _,measured=fixture(4)
        paths={'listado':('GET','/incidents'),'detalle':('GET','/incidents/00000000-0000-0000-0000-000000000001'),
            'creacion':('POST','/incidents'),'actualizacion':('PUT','/incidents/00000000-0000-0000-0000-000000000001/content')}
        for phase in ('calentamiento','medicion'):
            for op,(method,path) in paths.items():
                measured[phase]['metricas'][op]['intentos']=1
                complete(wrapper({'type':'http','method':method,'path':path,
                    'headers':[(b'x-qa-performance-phase',phase.encode())]},None,send))
        snapshot=wrapper.snapshot()
        for group in snapshot['grupos'].values():
            self.assertEqual(group['metricas']['pool_ping_calls']['media'],1)
            self.assertEqual(group['metricas']['consultas']['media'],1)
            self.assertEqual(group['metricas']['pool_ping_errors']['media'],0)
        self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(snapshot),measured),snapshot)
        self.assertNotIn('00000000-',json.dumps(snapshot))
