"""ConexiÃ³n PostgreSQL diferida; no carga archivos .env ni imprime secretos."""
import os
from functools import lru_cache

from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


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


def get_session():
    with Session(get_engine()) as session:
        yield session


def database_ready() -> bool:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
            revision = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            return revision == "0003"
    except (SQLAlchemyError, ValueError):
        return False
