"""Auditoría de departamentos sin alterar cuentas ni expedientes existentes."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("department_audit_events",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("department_id", sa.Uuid(), sa.ForeignKey("departamentos.id"), nullable=False),
        sa.Column("actor_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("detalle", postgresql.JSONB(), nullable=False),
        sa.Column("fecha", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_department_audit_events_department_id", "department_audit_events", ["department_id"])


def downgrade():
    raise RuntimeError("Reversión automática deshabilitada para preservar auditoría; requiere plan y respaldo")
