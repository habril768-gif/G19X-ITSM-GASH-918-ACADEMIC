"""CPU de workers QA: reloj del mismo hilo, contrato preservado y reportes3/4/5."""
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
import copy
import importlib.util
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

backend=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qa_cpu_timing',backend/'app/core/performance_timing.py')
timing=importlib.util.module_from_spec(spec);spec.loader.exec_module(timing)
sys.path.insert(0,str(backend/'scripts'))
import provision_performance_qa as provision
from test_performance_diagnostics import run_async
from test_performance_pool_ping import fixture


def state():
    row=dict.fromkeys(timing.FIELDS,0.0);row['thread_stages']={};return row


def v5_fixture():
    value,measured=fixture(4)
    value['version']=5;value['thread_cpu_instrumentado']=True
    for group in value['grupos'].values():
        group['metricas']['thread_cpu']={'media':1,'p95':1,'max':1}
        group['thread_stages']['other']['cpu_ms']=2
    return value,measured


class ThreadCPUTests(unittest.TestCase):
    def test_cpu_and_wall_are_separate_and_options_preserved(self):
        row=state();token=timing.current.set(row);calls=[];limiter=object()
        async def original(fn,*args,**kwargs):calls.append((args,kwargs));return fn(*args)
        try:
            with patch.object(timing.time,'perf_counter',side_effect=[0,.010,.050,.070]),patch.object(timing.time,'thread_time',side_effect=[100,100.004]):
                result=run_async(timing.instrument_threadpool(original)(lambda n:n+1,8,limiter=limiter,abandon_on_cancel=True))
        finally:timing.current.reset(token)
        self.assertEqual(result,9);self.assertEqual(calls,[((8,),{'limiter':limiter,'abandon_on_cancel':True})])
        self.assertAlmostEqual(row['thread_cpu'],4)
        self.assertAlmostEqual(row['thread_run'],40)
        self.assertAlmostEqual(row['thread_wait'],10)
        self.assertAlmostEqual(row['thread_resume'],20)
        self.assertAlmostEqual(row['thread_stages']['other']['cpu_ms'],4)

    def test_cpu_clock_is_read_twice_in_same_actual_worker(self):
        row=state();token=timing.current.set(row);ids=[];clock=timing.time.thread_time
        def measured_clock():ids.append(threading.get_ident());return clock()
        async def original(fn,*args,**kwargs):
            with ThreadPoolExecutor(max_workers=1) as pool:return pool.submit(copy_context().run,fn,*args).result()
        try:
            with patch.object(timing.time,'thread_time',measured_clock):
                self.assertEqual(run_async(timing.instrument_threadpool(original)(lambda:37)),37)
        finally:timing.current.reset(token)
        self.assertEqual(len(ids),2);self.assertEqual(ids[0],ids[1]);self.assertNotEqual(ids[0],threading.get_ident())
        self.assertGreaterEqual(row['thread_cpu'],0)
        self.assertEqual(row['thread_incomplete'],0)

    def test_unstarted_worker_does_not_read_cpu_clock(self):
        row=state();token=timing.current.set(row);error=ValueError('PRIVATE_NOT_STARTED')
        async def original(*args,**kwargs):raise error
        try:
            with patch.object(timing.time,'thread_time',side_effect=AssertionError('No iniciar reloj')):
                with self.assertRaises(ValueError) as caught:run_async(timing.instrument_threadpool(original)(lambda:None))
        finally:timing.current.reset(token)
        self.assertIs(caught.exception,error);self.assertEqual(row['thread_cpu'],0);self.assertEqual(row['thread_incomplete'],1)
        self.assertNotIn('PRIVATE',json.dumps(row))

    def test_failed_worker_records_cpu_and_preserves_exception_identity(self):
        row=state();token=timing.current.set(row);error=RuntimeError('PRIVATE_ERROR')
        async def original(fn,*args,**kwargs):return fn(*args)
        def fail():raise error
        try:
            with patch.object(timing.time,'thread_time',side_effect=[1,1.007]):
                with self.assertRaises(RuntimeError) as caught:run_async(timing.instrument_threadpool(original)(fail))
        finally:timing.current.reset(token)
        self.assertIs(caught.exception,error);self.assertAlmostEqual(row['thread_cpu'],7)
        self.assertEqual(row['thread_incomplete'],0);self.assertNotIn('PRIVATE',json.dumps(row))

    def test_summary_handles_cpu_and_legacy_rows(self):
        rows=[{'thread_stages':{'auth':{'calls':1,'wait_ms':0,'run_ms':3,'resume_ms':0,'incomplete':0}}},
              {'thread_stages':{'auth':{'calls':1,'wait_ms':0,'run_ms':3,'cpu_ms':2,'resume_ms':0,'incomplete':0}}}]
        result=timing.thread_summary(rows)['auth']
        self.assertEqual(result['cpu_ms'],2);self.assertEqual(result['cpu_ms_per_request'],1)
        self.assertEqual(result['run_ms_per_request'],3)

    def test_v3_v4_and_v5_valid_reports_are_readable(self):
        for version in (3,4):
            value,measured=fixture(version)
            self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(value),measured),value)
        value,measured=v5_fixture()
        self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(value),measured),value)

    def test_v5_requires_cpu_instrumentation_flag(self):
        for change in ('missing',False):
            value,measured=v5_fixture()
            if change=='missing':value.pop('thread_cpu_instrumentado')
            else:value['thread_cpu_instrumentado']=change
            with self.assertRaisesRegex(provision.ProvisionError,'CPU_HILO_AUSENTE'):
                provision.read_diagnostics(timing.MARKER+json.dumps(value),measured)

    def test_corrupt_cpu_stats_or_stage_totals_are_rejected(self):
        original,measured=v5_fixture()
        mutations=[lambda g:g['metricas'].pop('thread_cpu'),
            lambda g:g['metricas'].__setitem__('thread_cpu',{'media':float('nan'),'p95':1,'max':1}),
            lambda g:g['metricas'].__setitem__('thread_cpu',{'media':-1,'p95':1,'max':1}),
            lambda g:g['metricas'].__setitem__('thread_cpu',{'media':True,'p95':1,'max':1}),
            lambda g:g['metricas'].__setitem__('thread_cpu',{'media':3,'p95':1,'max':1}),
            lambda g:g['thread_stages']['other'].pop('cpu_ms'),
            lambda g:g['thread_stages']['other'].__setitem__('cpu_ms',float('inf')),
            lambda g:g['thread_stages']['other'].__setitem__('cpu_ms',-1),
            lambda g:g['thread_stages']['other'].__setitem__('cpu_ms',True),
            lambda g:g['thread_stages']['other'].__setitem__('cpu_ms',9)]
        for index,mutate in enumerate(mutations):
            value=copy.deepcopy(original);mutate(value['grupos']['medicion/creacion'])
            with self.subTest(index=index),self.assertRaises(provision.ProvisionError):
                provision.read_diagnostics(timing.MARKER+json.dumps(value),measured)

    def test_zero_cpu_is_allowed_for_clock_granularity(self):
        value,measured=v5_fixture()
        for group in value['grupos'].values():
            group['metricas']['thread_cpu']={'media':0,'p95':0,'max':0}
            group['thread_stages']['other']['cpu_ms']=0
        self.assertEqual(provision.read_diagnostics(timing.MARKER+json.dumps(value),measured),value)
