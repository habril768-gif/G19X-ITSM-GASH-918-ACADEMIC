"""Control SQL fijo: guard, medidas, limites y aislamiento; sin PostgreSQL real."""
from contextlib import contextmanager
import copy
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import performance_db_probe as probe
import provision_performance_qa as provision


class DBProbeTests(unittest.TestCase):
    def env(self):
        return dict(QA_PERF_DIAGNOSTIC_RUN_ID='qa123456',QA_PERF_DB_PROBE='true',
            POSTGRES_DB='plurione_test_perf_qa123456',POSTGRES_USER='qa_perf_qa123456',
            POSTGRES_HOST='postgres',AI_ENABLED='false',MAIL_ENABLED='false')

    def test_guard_requires_exact_isolated_identity_and_no_arbitrary_sql(self):
        self.assertEqual(probe.guard({'run_id':'qa123456'},self.env()),'qa123456')
        for key,value in [('POSTGRES_DB','plurione'),('POSTGRES_USER','operativo'),('POSTGRES_HOST','localhost'),
                          ('QA_PERF_DB_PROBE','false'),('QA_PERF_DIAGNOSTIC_RUN_ID','otro1234'),('AI_ENABLED','true'),('MAIL_ENABLED','true')]:
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'FUERA_QA'):
                probe.guard({'run_id':'qa123456'},dict(self.env(),**{key:value}))
        for payload in ({'run_id':'qa123456','sql':'PRIVATE_SQL'}, {'run_id':'../invalid'}, [], None):
            with self.assertRaises(ValueError):probe.guard(payload,self.env())

    def test_driver_cpu_and_server_times_are_separate_without_plan_leaks(self):
        calls=[]
        class Connection:
            def exec_driver_sql(self,sql):calls.append(sql);return self
            def scalar_one(self):return [{'Planning Time':.01,'Execution Time':.02,'Plan':{'PRIVATE_DATA':'hidden'}}]
        with patch.object(probe.time,'perf_counter',side_effect=[1,1.005]),patch.object(probe.time,'thread_time',side_effect=[3,3.001]):
            row=probe.measure(Connection())
        self.assertEqual(calls,[probe.EXPLAIN]);self.assertAlmostEqual(row['driver_ms'],5)
        self.assertAlmostEqual(row['worker_cpu_ms'],1);self.assertEqual(row['plan_ms'],.01);self.assertEqual(row['execution_ms'],.02)
        self.assertNotIn('PRIVATE',json.dumps(row))

    def test_control_has_exactly_fifty_five_readonly_samples_and_closes(self):
        calls=[];closed=[];lock=threading.Lock()
        class Connection:
            def exec_driver_sql(self,sql):
                with lock:calls.append(sql)
                return self
            def scalar_one(self):return [{'Planning Time':.01,'Execution Time':.02}]
        class Engine:
            @contextmanager
            def connect(self):
                try:yield Connection()
                finally:
                    with lock:closed.append(True)
        result=probe.run(Engine())
        self.assertEqual(result['grupos']['solo']['muestras'],5)
        self.assertEqual(result['grupos']['concurrente']['muestras'],50)
        self.assertEqual(calls.count(probe.EXPLAIN),55)
        self.assertEqual(calls.count('SET LOCAL statement_timeout = 3000'),11)
        self.assertEqual(len(closed),11)
        self.assertEqual(set(calls),{probe.EXPLAIN,'SET LOCAL statement_timeout = 3000'})

    def test_measure_rejects_invalid_server_data_and_preserves_driver_failure(self):
        class Connection:
            def __init__(self,value):self.value=value
            def exec_driver_sql(self,sql):return self
            def scalar_one(self):return self.value
        for data in (None,[],[{}],[{'Planning Time':-1,'Execution Time':0}],[{'Planning Time':float('nan'),'Execution Time':0}]):
            with self.assertRaises(ValueError):probe.measure(Connection(data))
        error=RuntimeError('PRIVATE_DRIVER')
        class Broken:
            def exec_driver_sql(self,sql):raise error
        with self.assertRaises(RuntimeError) as caught:probe.measure(Broken())
        self.assertIs(caught.exception,error)

    def test_probe_only_allowed_in_smoke_diagnostic_before_files(self):
        for diagnostic,mode in ((False,'smoke'),(True,'full')):
            with self.assertRaisesRegex(provision.ProvisionError,'SOLO'):
                provision.run(Path.cwd(),mode,'docker',diagnostic=diagnostic,db_probe=True)
        normal=provision.specification(Path.cwd(),'qa123456',18080)
        self.assertNotIn('QA_PERF_DB_PROBE',normal['services']['api']['environment'])
        special=provision.specification(Path.cwd(),'qa123456',18080,diagnostic=True,db_probe=True)
        self.assertEqual(special['services']['api']['environment']['QA_PERF_DB_PROBE'],'true')
        self.assertNotIn('command',special['services']['postgres'])

    def test_unexpected_output_fields_or_wrong_counts_are_rejected(self):
        metrics={f:{'media':0,'min':0,'p95':0,'max':0} for f in probe.METRICS}
        value={'version':1,'estado':'OK','limites':'Control','grupos':{name:{'clientes':clients,'muestras':5*clients,'metricas':copy.deepcopy(metrics)} for name,clients in (('solo',1),('concurrente',10))}}
        self.assertEqual(probe.validate(value),value)
        for mutate in (lambda v:v.update(sql='PRIVATE'),lambda v:v['grupos']['solo'].update(muestras=99),lambda v:v['grupos']['solo']['metricas']['driver_ms'].update(media=float('inf'))):
            invalid=copy.deepcopy(value);mutate(invalid)
            with self.assertRaises(ValueError):probe.validate(invalid)
