"""Verifica ping directo de pool SQLite y contrato del dialecto psycopg, sin PostgreSQL real."""
from types import SimpleNamespace
import unittest
from sqlalchemy import create_engine,event
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg
from app.core import performance_timing as timing


class PoolPingSQLAlchemyTests(unittest.TestCase):
    def test_reused_sqlite_connection_ping_bypasses_engine_sql_events(self):
        engine=create_engine('sqlite://',pool_pre_ping=True)
        self.addCleanup(engine.dispose)
        with engine.connect() as connection:
            raw=connection.connection.driver_connection
        traced=[];observed=[]
        raw.set_trace_callback(traced.append)
        engine.dialect.do_ping=timing.instrument_pool_ping(engine.dialect.do_ping)
        def before(conn,cursor,statement,parameters,context,executemany):observed.append(statement)
        event.listen(engine,'before_cursor_execute',before)
        row=dict.fromkeys(timing.FIELDS,0.0);token=timing.current.set(row)
        try:
            with engine.connect() as connection:self.assertEqual(connection.exec_driver_sql('SELECT 2').scalar_one(),2)
        finally:
            timing.current.reset(token);raw.set_trace_callback(None)
            event.remove(engine,'before_cursor_execute',before)
        self.assertEqual(observed,['SELECT 2'])
        self.assertIn('SELECT 1',traced);self.assertIn('SELECT 2',traced)
        self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,0))
        self.assertGreater(row['pool_ping'],0)

    def connection(self,error=None):
        calls=[]
        class Cursor:
            def execute(self,statement):
                calls.append('execute')
                if error:raise error
            def close(self):calls.append('close')
        connection=SimpleNamespace(autocommit=False,closed=False,cursor=lambda:Cursor())
        return connection,calls

    def test_psycopg_ping_preserves_autocommit_cursor_and_success(self):
        dialect=PGDialect_psycopg();connection,calls=self.connection()
        observed=timing.instrument_pool_ping(PGDialect_psycopg.do_ping)
        row=dict.fromkeys(timing.FIELDS,0.0);token=timing.current.set(row)
        try:self.assertIs(observed(dialect,connection),True)
        finally:timing.current.reset(token)
        self.assertFalse(connection.autocommit)
        self.assertEqual(calls,['execute','close'])
        self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,0))

    def test_psycopg_disconnect_still_classified_by_original_sqlalchemy_path(self):
        class Disconnected(Exception):pass
        error=Disconnected('PRIVATE_PASSWORD')
        dialect=PGDialect_psycopg()
        dialect.__dict__['loaded_dbapi']=SimpleNamespace(Error=Disconnected)
        dialect.is_disconnect=lambda err,connection,cursor:err is error
        dialect.do_ping=timing.instrument_pool_ping(dialect.do_ping)
        connection,calls=self.connection(error)
        row=dict.fromkeys(timing.FIELDS,0.0);token=timing.current.set(row)
        try:self.assertIs(dialect._do_ping_w_event(connection),False)
        finally:timing.current.reset(token)
        self.assertFalse(connection.autocommit)
        self.assertEqual(calls,['execute','close'])
        self.assertEqual((row['pool_ping_calls'],row['pool_ping_errors']),(1,1))
        self.assertNotIn('PRIVATE',str(row))
