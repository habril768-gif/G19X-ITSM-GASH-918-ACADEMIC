"""Entorno Alembic sin URL de conexión en archivos versionados."""
from alembic import context
from app.core.database import database_url, get_engine
from app.models import Base

if context.is_offline_mode():
    # El dialecto basta para compilar SQL; no se necesitan credenciales.
    context.configure(dialect_name="postgresql", target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with get_engine().connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
