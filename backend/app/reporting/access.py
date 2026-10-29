"""Cuenta nueva de lectura estricta; sin modificar privilegios globales existentes."""
import re
from psycopg import sql

class ReportingAccessError(Exception): pass

def provision(connection,username,password):
    if not re.fullmatch(r'[a-z][a-z0-9_]{2,47}',username) or not 16<=len(password)<=128:
        raise ReportingAccessError('Usuario de 3–48 caracteres y contraseña de 16–128 caracteres requeridos')
    raw=connection.connection.driver_connection
    with raw.cursor() as cursor:
        cursor.execute('SELECT current_database(), current_user')
        database,actor=cursor.fetchone()
        cursor.execute('SELECT 1 FROM pg_catalog.pg_roles WHERE rolname=%s',(username,))
        if cursor.fetchone() is not None:
            raise ReportingAccessError('La cuenta ya existe; no se modificaron sus permisos o contraseña')
        cursor.execute(sql.SQL('CREATE ROLE {} LOGIN PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT NOREPLICATION NOBYPASSRLS').format(sql.Identifier(username),sql.Literal(password)))
        cursor.execute(sql.SQL('GRANT CONNECT ON DATABASE {} TO {}').format(sql.Identifier(database),sql.Identifier(username)))
        cursor.execute(sql.SQL('GRANT USAGE ON SCHEMA analytics TO {}').format(sql.Identifier(username)))
        cursor.execute(sql.SQL('GRANT SELECT ON analytics.incident_metrics, analytics.export_info TO {}').format(sql.Identifier(username)))
        cursor.execute(sql.SQL('ALTER ROLE {} SET default_transaction_read_only=on').format(sql.Identifier(username)))
        cursor.execute(sql.SQL("ALTER ROLE {} SET statement_timeout='30s'").format(sql.Identifier(username)))
        cursor.execute("SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_class c JOIN pg_catalog.pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relkind IN ('r','p','v','m') AND has_table_privilege(%s,c.oid,'SELECT,INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER'))",(username,))
        if cursor.fetchone()[0]:
            raise ReportingAccessError('Existen privilegios heredados de PUBLIC sobre datos operativos; revise la configuración sin ampliar permisos')
        cursor.execute("SELECT has_schema_privilege(%s,'public','CREATE') OR has_schema_privilege(%s,'analytics','CREATE') OR has_database_privilege(%s,current_database(),'CREATE')",(username,username,username))
        if cursor.fetchone()[0]:
            raise ReportingAccessError('Existen permisos globales de creación; revise la configuración antes de usar analítica')
