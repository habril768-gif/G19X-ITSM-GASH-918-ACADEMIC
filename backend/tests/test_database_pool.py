"""Pool base: retencion acotada y limite conservado, puente SQLite sin PostgreSQL."""
from concurrent.futures import ThreadPoolExecutor
import threading
import unittest
from unittest.mock import patch
from sqlalchemy import URL,create_engine,event
from sqlalchemy.exc import TimeoutError as PoolTimeoutError
from sqlalchemy.pool import QueuePool
from app.core import database


class DatabasePoolTests(unittest.TestCase):
    def setUp(self):
        database.get_engine.cache_clear()
        self.created=[];self.options=None
        def local_engine(url,**options):
            self.options=dict(options)
            # El URL/timeout de conexion PostgreSQL no se usan para abrir red.
            local=dict(options,connect_args={'check_same_thread':False})
            engine=create_engine('sqlite://',poolclass=QueuePool,**local)
            self.created.append(engine)
            return engine
        self.patches=[patch.object(database,'database_url',return_value=URL.create('postgresql+psycopg',username='qa',password='ficticio',host='postgres',database='qa')),
                      patch.object(database,'create_engine',side_effect=local_engine)]
        for item in self.patches:item.start()

    def tearDown(self):
        for engine in self.created:engine.dispose()
        database.get_engine.cache_clear()
        for item in reversed(self.patches):item.stop()

    def waves(self,engine,rounds=3):
        created=[];lock=threading.Lock();output=[]
        def connect(*args):
            with lock:created.append(True)
        event.listen(engine,'connect',connect)
        try:
            with ThreadPoolExecutor(max_workers=10) as workers:
                for _ in range(rounds):
                    barrier=threading.Barrier(10);before=len(created)
                    def work():
                        with engine.connect() as connection:
                            value=connection.exec_driver_sql('SELECT 1').scalar_one()
                            barrier.wait(timeout=10)
                            return value
                    futures=[workers.submit(work) for _ in range(10)]
                    self.assertEqual([future.result(timeout=15) for future in futures],[1]*10)
                    output.append(len(created)-before)
        finally:event.remove(engine,'connect',connect)
        return output

    def test_engine_is_lazy_cached_and_retains_original_connection_limits(self):
        engine=database.get_engine()
        self.assertIs(database.get_engine(),engine);self.assertEqual(len(self.created),1)
        self.assertEqual(engine.pool.checkedin(),0);self.assertEqual(engine.pool.checkedout(),0)
        self.assertEqual(engine.pool.size(),5)
        self.assertEqual(engine.pool.size()+engine.pool._max_overflow,15)
        self.assertTrue(self.options['pool_pre_ping'])
        self.assertEqual(engine.pool.timeout(),30)
        self.assertEqual(self.options['connect_args'],{'connect_timeout':3})

    def test_ten_concurrent_connections_keep_idle_pool_bounded(self):
        engine=database.get_engine()
        self.assertEqual(self.waves(engine),[10,5,5])
        self.assertEqual(engine.pool.checkedin(),5);self.assertEqual(engine.pool.checkedout(),0)

    def test_sixteenth_connection_cannot_exceed_original_limit(self):
        engine=database.get_engine();engine.pool._timeout=.05  # Solo prueba: fallar rapido.
        held=[]
        try:
            held=[engine.connect() for _ in range(15)]
            self.assertEqual(engine.pool.checkedout(),15)
            with self.assertRaises(PoolTimeoutError):engine.connect()
            self.assertEqual(engine.pool.checkedout(),15)
        finally:
            for connection in held:connection.close()
        self.assertEqual(engine.pool.checkedout(),0);self.assertEqual(engine.pool.checkedin(),5)

    def test_pre_ping_still_recovers_stale_connection(self):
        engine=database.get_engine();created=[]
        def connect(*args):created.append(True)
        event.listen(engine,'connect',connect)
        try:
            with engine.connect() as connection:raw=connection.connection.driver_connection
            raw.close()  # Simular conexion ociosa cerrada por servidor.
            with engine.connect() as connection:self.assertEqual(connection.exec_driver_sql('SELECT 1').scalar_one(),1)
            self.assertEqual(len(created),2)
        finally:event.remove(engine,'connect',connect)

    def test_saturated_pool_reuses_returned_connection_without_extra_capacity(self):
        engine=database.get_engine();created=[];held=[];started=threading.Event()
        def connect(*args):created.append(True)
        event.listen(engine,'connect',connect)
        try:
            held=[engine.connect() for _ in range(15)]
            def work():
                started.set()
                with engine.connect() as connection:return connection.exec_driver_sql('SELECT 1').scalar_one()
            with ThreadPoolExecutor(max_workers=1) as workers:
                future=workers.submit(work)
                try:
                    self.assertTrue(started.wait(timeout=2))
                finally:held.pop().close()
                self.assertEqual(future.result(timeout=2),1)
            self.assertEqual(len(created),15)
        finally:
            for connection in held:connection.close()
            event.remove(engine,'connect',connect)
        self.assertEqual(engine.pool.checkedout(),0)

    def test_dispose_closes_all_retained_idle_connections(self):
        engine=database.get_engine();closed=[]
        self.waves(engine,rounds=1)
        def close(*args):closed.append(True)
        event.listen(engine,'close',close)
        try:engine.dispose()
        finally:event.remove(engine,'close',close)
        self.assertEqual(len(closed),5)
        self.assertEqual(engine.pool.checkedin(),0)
