"""Esquema inicial PostgreSQL; reglas de autorizaciÃ³n se implementan en servicios."""
from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, Boolean, CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, Uuid, func, column, false, true
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
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true())


class DepartmentAudit(Base):
    """Historial administrativo separado de los expedientes personales."""
    __tablename__ = "department_audit_events"
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"), index=True)
    actor_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    detalle: Mapped[dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "external_id", name="uq_users_entra"),
        CheckConstraint("(tenant_id IS NULL) = (external_id IS NULL)", name="ck_users_identity_pair"),
        Index("uq_users_email_lower", func.lower(column("email")), unique=True),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(320))
    external_id: Mapped[UUID | None] = mapped_column(Uuid)
    tenant_id: Mapped[UUID | None] = mapped_column(Uuid)
    nombre_completo: Mapped[str] = mapped_column(String(200))
    departamento_id: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"), index=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=true())


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
        CheckConstraint("ai_status IN ('PENDIENTE','COMPLETADA','FALLIDA','OMITIDA')", name="ck_incident_ai_status"),
        CheckConstraint("status = 'PENDIENTE' OR (assigned_to IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL AND cycle_start_at IS NOT NULL)", name="ck_incident_assigned"),
        CheckConstraint("status NOT IN ('RESUELTA','CERRADA') OR (resolved_at IS NOT NULL AND length(trim(resolution_text)) > 0 AND resolution_text IS NOT NULL AND validated_by IS NOT NULL AND validated_at IS NOT NULL)", name="ck_incident_resolution"),
        CheckConstraint("status != 'CERRADA' OR closed_at IS NOT NULL", name="ck_incident_closed"),
        CheckConstraint("scope IN ('PERSONA','ENTORNO')", name="ck_incident_scope"),
        CheckConstraint("(scope = 'PERSONA' AND affected_employee_id IS NOT NULL) OR (scope = 'ENTORNO' AND affected_employee_id IS NULL)", name="ck_incident_affected_scope"),
        CheckConstraint("scope != 'ENTORNO' OR category_id IS NULL OR category_id = 4", name="ck_incident_environment_category"),
        CheckConstraint("NOT classification_valid OR (validated_by IS NOT NULL AND validated_at IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL)", name="ck_incident_classification_valid"),
        CheckConstraint("status NOT IN ('RESUELTA','CERRADA') OR classification_valid", name="ck_incident_resolved_validation"),
        CheckConstraint("ai_status != 'OMITIDA' OR (ai_skip_reason IS NOT NULL AND length(trim(ai_skip_reason)) > 0)", name="ck_incident_ai_skip"),
        CheckConstraint("(ai_input_reviewed_by IS NULL AND ai_input_reviewed_at IS NULL) OR (ai_input_reviewed_by IS NOT NULL AND ai_input_reviewed_at IS NOT NULL AND ai_input_text IS NOT NULL AND length(trim(ai_input_text)) > 0)", name="ck_incident_ai_review"),
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
    ai_suggestion: Mapped[dict | None] = mapped_column(JSONB().with_variant(JSON(), "sqlite"))
    ai_error: Mapped[str | None] = mapped_column(Text)
    ai_status: Mapped[str] = mapped_column(String(20), server_default="PENDIENTE")
    validated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolution_text: Mapped[str | None] = mapped_column(Text)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cycle_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reopening_reason: Mapped[str | None] = mapped_column(Text)
    is_confidential: Mapped[bool] = mapped_column(Boolean, server_default=false())
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    affected_employee_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    assigned_to: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"), index=True)
    department_id_at_creation: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"))
    scope: Mapped[str] = mapped_column(String(10), server_default="PERSONA")
    reported_department_id: Mapped[UUID] = mapped_column(ForeignKey("departamentos.id"), index=True)
    classification_valid: Mapped[bool] = mapped_column(Boolean, server_default=false())
    ai_input_text: Mapped[str | None] = mapped_column(Text)
    ai_input_reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    ai_input_reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ai_skip_reason: Mapped[str | None] = mapped_column(Text)
    ai_model: Mapped[str | None] = mapped_column(String(120))
    ai_prompt_version: Mapped[str | None] = mapped_column(String(80))
    content_revision: Mapped[int] = mapped_column(Integer, server_default="0")


class AIJob(Base):
    __tablename__ = "ai_jobs"
    __table_args__ = (
        UniqueConstraint("case_id", "input_digest", name="uq_ai_job_input"),
        CheckConstraint("status IN ('PENDIENTE','EN_PROCESO','COMPLETADA','FALLIDA','OMITIDA')", name="ck_ai_job_status"),
        CheckConstraint("attempts BETWEEN 0 AND 3", name="ck_ai_job_attempts"),
        Index("ix_ai_jobs_due", "status", "available_at"),
    )
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    case_id: Mapped[UUID] = mapped_column(ForeignKey("incidencias.id"), index=True)
    reviewed_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    input_text: Mapped[str] = mapped_column(Text)
    input_digest: Mapped[str] = mapped_column(String(64))
    content_revision: Mapped[int] = mapped_column(Integer)
    catalog: Mapped[list] = mapped_column(JSONB().with_variant(JSON(), "sqlite"))
    model: Mapped[str] = mapped_column(String(120))
    prompt_version: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(20), server_default="PENDIENTE")
    attempts: Mapped[int] = mapped_column(Integer, server_default="0")
    available_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    lease_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    lease_token: Mapped[UUID | None] = mapped_column(Uuid)
    dispatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    result: Mapped[dict | None] = mapped_column(JSONB().with_variant(JSON(), "sqlite"))
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))



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
    detalle: Mapped[dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"))
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class LocalCredential(Base):
    __tablename__ = "local_credentials"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    password_hash: Mapped[str] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AuthSession(Base):
    __tablename__ = "auth_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class LoginThrottle(Base):
    __tablename__ = "login_throttle"
    email: Mapped[str] = mapped_column(String(320), primary_key=True)
    failures: Mapped[int] = mapped_column(Integer, server_default="0")
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class IncidentParticipant(Base):
    """Relación declarada; autorización y recusa requieren servicio transaccional."""
    __tablename__ = "incident_involved_users"
    __table_args__ = (
        CheckConstraint("review_status IN ('DECLARADO','CONFIRMADO','DESCARTADO')", name="ck_participant_status"),
        CheckConstraint("length(trim(declaration_reason)) > 0", name="ck_participant_declaration"),
        CheckConstraint("(review_status = 'DECLARADO' AND reviewed_by IS NULL AND reviewed_at IS NULL AND review_reason IS NULL) OR (review_status IN ('CONFIRMADO','DESCARTADO') AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL AND review_reason IS NOT NULL AND length(trim(review_reason)) > 0)", name="ck_participant_review"),
        CheckConstraint("reviewed_by IS NULL OR reviewed_by != user_id", name="ck_participant_no_self_review"),
    )
    incidencia_id: Mapped[UUID] = mapped_column(ForeignKey("incidencias.id"), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True, index=True)
    review_status: Mapped[str] = mapped_column(String(20), server_default="DECLARADO")
    declaration_reason: Mapped[str] = mapped_column(Text)
    reviewed_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    review_reason: Mapped[str | None] = mapped_column(Text)
