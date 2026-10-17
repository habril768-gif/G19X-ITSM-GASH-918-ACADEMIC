"""Coordina cambios administrativos con mutaciones de expedientes en PostgreSQL."""
from fastapi import HTTPException
from sqlalchemy import text
from app.models import Department


def administration_lock(db, actor=None, exclusive=False):
    if db.bind.dialect.name == "postgresql":
        function = "pg_advisory_xact_lock" if exclusive else "pg_advisory_xact_lock_shared"
        db.execute(text(f"SELECT {function}(71419322)"))
    if actor is not None:
        db.refresh(actor)
        department = db.get(Department, actor.departamento_id)
        if department is not None:
            db.refresh(department)
        if not actor.is_active or department is None or not department.is_active:
            raise HTTPException(403, "Cuenta no habilitada")
