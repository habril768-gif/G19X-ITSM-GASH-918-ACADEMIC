"""Esquema inicial PostgreSQL; reglas de autorización se implementan en servicios."""
from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True)


class Department(Base):
    __tablename__ = "departamentos"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    nombre: Mapped[str] = mapped_column(String(120), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("tenant_id", "external_id", name="uq_users_entra"),)
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320))
    external_id: Mapped[UUID] = mapped_column(Uuid)
    tenant_id: Mapped[UUID] = mapped_column(Uuid)
    nombre_completo: Mapped[str] = mapped_column(String(200))
    departamento_id: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"), index=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true")


class Category(Base):
    __tablename__ = "categorias_incidencia"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    descripcion: Mapped[str] = mapped_column(Text)


class Incident(Base):
    __tablename__ = "incidencias"
    __table_args__ = (
        CheckConstraint("status IN ('PENDIENTE','EN_REVISION','RESUELTA','CERRADA')", name="ck_incident_status"),
        CheckConstraint("priority IS NULL OR priority IN (1,2,3)", name="ck_incident_priority"),
        CheckConstraint("ai_status IN ('PENDIENTE','COMPLETADA','FALLIDA')", name="ck_incident_ai_status"),
        CheckConstraint("status = 'PENDIENTE' OR (assigned_to IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL AND cycle_start_at IS NOT NULL)", name="ck_incident_assigned"),
        CheckConstraint("status NOT IN ('RESUELTA','CERRADA') OR (resolved_at IS NOT NULL AND length(trim(resolution_text)) > 0 AND resolution_text IS NOT NULL AND validated_by IS NOT NULL AND validated_at IS NOT NULL)", name="ck_incident_resolution"),
        CheckConstraint("status != 'CERRADA' OR closed_at IS NOT NULL", name="ck_incident_closed"),
        Index("ix_incident_status_priority", "status", "priority"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    titulo: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str] = mapped_column(Text)
    incident_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status: Mapped[str] = mapped_column(String(20), server_default="PENDIENTE")
    priority: Mapped[int | None] = mapped_column(Integer)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categorias_incidencia.id"))
    ai_suggestion: Mapped[dict | None] = mapped_column(JSONB)
    ai_error: Mapped[str | None] = mapped_column(Text)
    ai_status: Mapped[str] = mapped_column(String(20), server_default="PENDIENTE")
    validated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolution_text: Mapped[str | None] = mapped_column(Text)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cycle_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reopening_reason: Mapped[str | None] = mapped_column(Text)
    is_confidential: Mapped[bool] = mapped_column(Boolean, server_default="false")
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    affected_employee_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    assigned_to: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    department_id_at_creation: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"))


class AuditEvent(Base):
    __tablename__ = "historial_incidencias"
    __table_args__ = (
        CheckConstraint("accion IN ('CREADO','ESTADO_CAMBIADO','ASIGNADO','REAPERTURA','VALIDACION_IA','CAMBIO_CONFIDENCIALIDAD','CONTENIDO_EDITADO','USUARIO_ACTUALIZADO')", name="ck_audit_action"),
        CheckConstraint("incidencia_id IS NOT NULL OR affected_user_id IS NOT NULL", name="ck_audit_target"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    incidencia_id: Mapped[UUID | None] = mapped_column(ForeignKey("incidencias.id"), index=True)
    affected_user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    usuario_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    accion: Mapped[str] = mapped_column(String(40))
    detalle: Mapped[dict] = mapped_column(JSONB)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
