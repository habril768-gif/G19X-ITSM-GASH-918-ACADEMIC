"""Entrada ASGI opcional solo para QA aislado; app.main permanece sin instrumentar."""
import os
import time
from app.core.performance_timing import Timing, add_sql, current, guard, instrument_pool_ping, instrument_threadpool, sql_family, timed

guard(os.environ)

# Parche solo en este proceso QA protegido; app.main no importa este módulo.
import anyio.to_thread
anyio.to_thread.run_sync = instrument_threadpool(anyio.to_thread.run_sync)

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg

# El ping del pool usa directamente DBAPI, sin before_cursor_execute.
# Este parche existe solo después de guard QA y conserva manejo de desconexión.
PGDialect_psycopg.do_ping = instrument_pool_ping(PGDialect_psycopg.do_ping)
from fastapi.routing import APIRoute
from app.main import create_app
from app.core.security import current_user


@event.listens_for(Engine, "before_cursor_execute")
def before_sql(conn, cursor, statement, parameters, context, executemany):
    state = current.get()
    if state is not None:
        context._qa_perf_family = sql_family(statement)
        context._qa_perf_start = time.perf_counter()
        state["consultas"] += 1


def finish_sql(context):
    state = current.get()
    if state is not None and hasattr(context, "_qa_perf_start"):
        elapsed = (time.perf_counter() - context._qa_perf_start) * 1000
        add_sql(state, context._qa_perf_family, elapsed)
        del context._qa_perf_family
        del context._qa_perf_start


@event.listens_for(Engine, "after_cursor_execute")
def after_sql(conn, cursor, statement, parameters, context, executemany):
    finish_sql(context)


@event.listens_for(Engine, "handle_error")
def failed_sql(exception_context):
    if exception_context.execution_context is not None:
        finish_sql(exception_context.execution_context)


@event.listens_for(Session, "before_commit")
def before_commit(session):
    state = current.get()
    if state is not None:
        state["commit_start"] = time.perf_counter()


@event.listens_for(Session, "after_commit")
def after_commit(session):
    state = current.get()
    if state is not None and "commit_start" in state:
        state["commit"] += (time.perf_counter() - state.pop("commit_start")) * 1000


# Instrumentar el router fuente antes de incluirlo: FastAPI 0.143 crea
# contextos efectivos de rutas de forma diferida a partir de route.endpoint.
from app.api.incidents import router as incidents_router
for route in incidents_router.routes:
    if isinstance(route, APIRoute):
        endpoint = route.endpoint
        if hasattr(endpoint, "with_response_worker"):
            # El trabajo y su DTO se cronometran dentro del worker; conservar
            # ruta async para no reintroducir validación en otro hilo.
            route.endpoint = endpoint.with_response_worker(timed("endpoint", endpoint.response_worker))
        else:
            route.endpoint = timed("endpoint", endpoint)
        route.dependant.call = route.endpoint
inner = create_app()
inner.dependency_overrides[current_user] = timed("auth", current_user)
app = Timing(inner, pool_ping_instrumented=True, thread_cpu_instrumented=True)
