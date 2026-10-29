"""Instrumentación agregada exclusiva del diagnóstico QA; solo biblioteca estándar."""
from contextvars import ContextVar
from functools import wraps
import json
import math
import re
import threading
import time
from uuid import UUID

MARKER = "QA_PERF_DIAGNOSTICS_JSON="
current = ContextVar("qa_performance_timing", default=None)
FIELDS = ("total", "auth", "endpoint", "sql", "commit", "fuera_auth_endpoint", "consultas", "hasta_envio", "cierre", "thread_calls", "thread_wait", "thread_run", "thread_resume", "thread_incomplete", "thread_cpu", "pool_ping", "pool_ping_calls", "pool_ping_errors")


def guard(env):
    run_id = env.get("QA_PERF_DIAGNOSTIC_RUN_ID", "")
    if not (re.fullmatch(r"[a-z0-9]{8,24}", run_id)
            and env.get("POSTGRES_DB") == "plurione_test_perf_" + run_id
            and env.get("POSTGRES_USER") == "qa_perf_" + run_id
            and env.get("POSTGRES_HOST") == "postgres"
            and env.get("AI_ENABLED") == "false" and env.get("MAIL_ENABLED") == "false"):
        raise RuntimeError("DIAGNOSTICO_FUERA_DE_QA")


def operation(method, path):
    if path == "/incidents":
        return {"GET": "listado", "POST": "creacion"}.get(method)
    parts = path.strip("/").split("/")
    if len(parts) not in (2, 3) or parts[0] != "incidents":
        return None
    try:
        UUID(parts[1])
    except ValueError:
        return None
    if len(parts) == 2 and method == "GET":
        return "detalle"
    if len(parts) == 3 and parts[2] == "content" and method == "PUT":
        return "actualizacion"
    return None


def timed(name, function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        state = current.get()
        if state is None:
            return function(*args, **kwargs)
        start = time.perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            state[name] += (time.perf_counter() - start) * 1000
    return wrapped


def instrument_pool_ping(do_ping):
    """Solo QA: conserva resultado/excepcion y no guarda conexion o argumentos."""
    @wraps(do_ping)
    def observed(*args, **kwargs):
        state = current.get()
        if state is None:
            return do_ping(*args, **kwargs)
        start = time.perf_counter()
        state["pool_ping_calls"] += 1
        try:
            result = do_ping(*args, **kwargs)
            if result is False:
                state["pool_ping_errors"] += 1
            return result
        except BaseException:
            state["pool_ping_errors"] += 1
            raise
        finally:
            state["pool_ping"] += (time.perf_counter() - start) * 1000
    return observed



# Solo etiquetas de tablas conocidas: nunca guardar SQL, parámetros o literales.
TABLES = ("roles", "departamentos", "department_audit_events", "users", "categorias_incidencia",
    "incidencias", "ai_jobs", "historial_incidencias", "local_credentials", "auth_sessions",
    "login_throttle", "incident_involved_users", "mail_deliveries")
TABLE_PATTERNS = {table: re.compile(r'\b(?:from|join|update|into)\s+"?' + table + r'"?\b', re.I)
                  for table in TABLES}


def sql_family(statement):
    # El texto solo se inspecciona en memoria; la salida procede de allowlists.
    verb = statement.lstrip().split(None, 1)[0].upper() if statement.strip() else "OTHER"
    if verb not in {"SELECT", "INSERT", "UPDATE", "DELETE"}:
        verb = "OTHER"
    if verb == "SELECT" and ("pg_advisory_xact_lock(" in statement or "pg_advisory_xact_lock_shared(" in statement):
        return "SELECT/advisory_lock"
    names = [table for table, pattern in TABLE_PATTERNS.items() if pattern.search(statement)]
    return verb + "/" + ("+".join(names) if names else "otras")


def add_sql(state, family, elapsed):
    state["sql"] += elapsed
    bucket = state["familias_sql"].setdefault(family, {"consultas": 0, "ms": 0.0})
    bucket["consultas"] += 1
    bucket["ms"] += elapsed


def family_summary(rows):
    result = {}
    for row in rows:
        for family, entry in row.get("familias_sql", {}).items():
            bucket = result.setdefault(family, {"consultas": 0, "ms": 0.0})
            bucket["consultas"] += entry["consultas"]
            bucket["ms"] += entry["ms"]
    for entry in result.values():
        entry["consultas_por_peticion"] = entry["consultas"] / len(rows)
        entry["ms_por_peticion"] = entry["ms"] / len(rows)
        entry["ms_por_consulta"] = entry["ms"] / entry["consultas"]
    return result



THREAD_STAGES = ("auth", "endpoint", "response_validation", "dependency_enter", "dependency_exit", "other")


def thread_stage(function):
    # Solo categorías fijas; nunca nombres arbitrarios, argumentos o resultados.
    for _ in range(8):
        if hasattr(function, "func"):
            function = function.func
        else:
            break
    name = getattr(function, "__name__", "")
    module = getattr(function, "__module__", "")
    if name == "current_user": return "auth"
    if name == "_run_sync_endpoint" or (name == "_run_validated_endpoint" and module == "app.core.worker_response"): return "endpoint"
    if name == "validate" and module.startswith("fastapi."): return "response_validation"
    if name == "__enter__": return "dependency_enter"
    if name == "__exit__": return "dependency_exit"
    return "other"


def instrument_threadpool(run_sync):
    @wraps(run_sync)
    async def observed(function, *args, **kwargs):
        state = current.get()
        if state is None:
            return await run_sync(function, *args, **kwargs)
        category = thread_stage(function)
        slot = {}
        scheduled = time.perf_counter()
        def worker(*actual_args):
            slot["start"] = time.perf_counter()
            slot["cpu_start"] = time.thread_time()
            try:
                return function(*actual_args)
            finally:
                slot["cpu_end"] = time.thread_time()
                slot["end"] = time.perf_counter()
        try:
            # Conservar limiter y opciones de cancelación; no reintentar llamadas.
            return await run_sync(worker, *args, **kwargs)
        finally:
            resumed = time.perf_counter()
            complete = "end" in slot
            values = {"calls": 1, "incomplete": 0 if complete else 1,
                "wait_ms": max(0, (slot["start"] - scheduled) * 1000) if "start" in slot else 0,
                "run_ms": max(0, (slot["end"] - slot["start"]) * 1000) if complete else 0,
                "cpu_ms": max(0, (slot["cpu_end"] - slot["cpu_start"]) * 1000) if complete else 0,
                "resume_ms": max(0, (resumed - slot["end"]) * 1000) if complete else 0}
            bucket = state["thread_stages"].setdefault(category, dict.fromkeys(values, 0))
            for key, value in values.items(): bucket[key] += value
            for field, key in (("thread_calls", "calls"), ("thread_incomplete", "incomplete"),
                    ("thread_wait", "wait_ms"), ("thread_run", "run_ms"), ("thread_resume", "resume_ms"), ("thread_cpu", "cpu_ms")):
                state[field] += values[key]
    return observed


def thread_summary(rows):
    result = {}
    for row in rows:
        for category, values in row.get("thread_stages", {}).items():
            bucket = result.setdefault(category, dict.fromkeys(values, 0))
            for key, value in values.items(): bucket[key] = bucket.get(key, 0) + value
    for values in result.values():
        values["calls_per_request"] = values["calls"] / len(rows)
        for field in ("wait_ms", "run_ms", "resume_ms", "cpu_ms"):
            values[field + "_per_request"] = values.get(field, 0) / len(rows)
    return result


class Timing:
    def __init__(self, app, *, pool_ping_instrumented=False, thread_cpu_instrumented=False):
        self.app = app
        self.pool_ping_instrumented = pool_ping_instrumented
        self.thread_cpu_instrumented = thread_cpu_instrumented
        self.rows = {}
        self.lock = threading.Lock()
        self.overflow = False

    def snapshot(self):
        with self.lock:
            result = {}
            for key, rows in self.rows.items():
                result[key] = {"solicitudes": len(rows),
                    "errores": sum(r["status"] not in (200, 201) for r in rows), "metricas": {}}
                for field in FIELDS:
                    values = sorted(r[field] for r in rows)
                    result[key]["metricas"][field] = {"media": sum(values) / len(values),
                        "p95": values[math.ceil(.95 * len(values)) - 1], "max": values[-1]}
                result[key]["familias_sql"] = family_summary(rows)
                result[key]["thread_stages"] = thread_summary(rows)
            return {"version": 5, "thread_cpu_instrumentado": self.thread_cpu_instrumented, "pool_ping_instrumentado": self.pool_ping_instrumented, "limite_excedido": self.overflow, "grupos": result,
                "unidades": "ms salvo consultas, thread_calls, thread_incomplete, pool_ping_calls y pool_ping_errors (cantidad)",
                "limites": "SQL, commit y pool_ping son subconjuntos solapados de auth/endpoint. consultas excluye pool_ping, BEGIN/COMMIT/ROLLBACK del driver y nuevas conexiones. No sumar sus p95. thread_cpu mide CPU del worker, no PostgreSQL/otros hilos; diferencia con thread_run incluye esperas y planificación, no identifica una causa única. Total cubre ASGI, no red/cliente. Instrumentación añade coste; no acredita RNF-2."}

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            async def lifespan_send(message):
                if message["type"] == "lifespan.shutdown.complete":
                    print(MARKER + json.dumps(self.snapshot(), separators=(",", ":")), flush=True)
                await send(message)
            return await self.app(scope, receive, lifespan_send)
        headers = dict(scope.get("headers", []))
        phase = headers.get(b"x-qa-performance-phase", b"")
        op = operation(scope.get("method"), scope.get("path", ""))
        if scope["type"] != "http" or phase not in (b"calentamiento", b"medicion") or op is None:
            return await self.app(scope, receive, send)
        state = dict.fromkeys(FIELDS, 0.0)
        state["status"] = 500
        state["familias_sql"] = {}
        state["thread_stages"] = {}
        token = current.set(state)
        start = time.perf_counter()
        async def observed_send(message):
            if message["type"] == "http.response.start":
                state["status"] = message["status"]
            await send(message)
            if message["type"] == "http.response.body" and not message.get("more_body", False):
                state["hasta_envio"] = (time.perf_counter() - start) * 1000
        try:
            return await self.app(scope, receive, observed_send)
        finally:
            state["total"] = (time.perf_counter() - start) * 1000
            state["fuera_auth_endpoint"] = max(0, state["total"] - state["auth"] - state["endpoint"])
            if state["hasta_envio"]:
                state["cierre"] = max(0, state["total"] - state["hasta_envio"])
            current.reset(token)
            with self.lock:
                rows = self.rows.setdefault(phase.decode("ascii") + "/" + op, [])
                if len(rows) < 100000:
                    rows.append({field: state[field] for field in (*FIELDS, "status", "familias_sql", "thread_stages")})
                else:
                    self.overflow = True
