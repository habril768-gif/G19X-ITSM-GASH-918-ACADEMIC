"""Conexión PostgreSQL diferida; no carga archivos .env ni imprime secretos."""
import os
from functools import lru_cache

import anyio.to_thread

from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# Mantener referencia a la clase estándar: sesiones custom conservan worker.
_BASE_SESSION_TYPE = Session


def database_url() -> URL:
    password = os.environ.get("POSTGRES_PASSWORD")
    if not password:
        raise ValueError("Falta configurar PostgreSQL")
    return URL.create(
        "postgresql+psycopg",
        username=os.environ.get("POSTGRES_USER", "plurione"),
        password=password,
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        database=os.environ.get("POSTGRES_DB", "plurione"),
    )


@lru_cache
def get_engine():
    return create_engine(database_url(), pool_pre_ping=True, connect_args={"connect_timeout": 3})


async def get_session():
    # Construir Session no abre una conexión; las consultas siguen en workers.
    session = Session(get_engine())
    try:
        yield session
    finally:
        with anyio.CancelScope(shield=True):
            if type(session) is _BASE_SESSION_TYPE and not session.in_transaction():
                # Sin transacción no quedan conexiones en esta Session estándar:
                # close solo separa objetos ORM, sin SQL, rollback o checkin.
                session.close()
            else:
                # Lecturas, transacciones pendientes y sesiones custom pueden
                # hacer IO. Limiter independiente para evitar bloqueo del cierre.
                await anyio.to_thread.run_sync(session.close, limiter=anyio.CapacityLimiter(1))


def database_ready() -> bool:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
            revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            return revision == "0008"
    except (SQLAlchemyError, ValueError):
        return False
