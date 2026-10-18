"""Trabajos IA durables y versión del contenido; no envía textos existentes."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('incidencias', sa.Column('content_revision', sa.Integer(), server_default='0', nullable=False))
    op.create_table('ai_jobs',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('case_id', sa.Uuid(), sa.ForeignKey('incidencias.id'), nullable=False),
        sa.Column('reviewed_by', sa.Uuid(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('input_text', sa.Text(), nullable=False),
        sa.Column('input_digest', sa.String(64), nullable=False),
        sa.Column('content_revision', sa.Integer(), nullable=False),
        sa.Column('catalog', postgresql.JSONB(), nullable=False),
        sa.Column('model', sa.String(120), nullable=False),
        sa.Column('prompt_version', sa.String(80), nullable=False),
        sa.Column('status', sa.String(20), server_default='PENDIENTE', nullable=False),
        sa.Column('attempts', sa.Integer(), server_default='0', nullable=False),
        sa.Column('available_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('lease_until', sa.DateTime(timezone=True)), sa.Column('lease_token', sa.Uuid()),
        sa.Column('dispatched_at', sa.DateTime(timezone=True)),
        sa.Column('result', postgresql.JSONB()), sa.Column('error', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.UniqueConstraint('case_id', 'input_digest', name='uq_ai_job_input'),
        sa.CheckConstraint("status IN ('PENDIENTE','EN_PROCESO','COMPLETADA','FALLIDA','OMITIDA')", name='ck_ai_job_status'),
        sa.CheckConstraint('attempts BETWEEN 0 AND 3', name='ck_ai_job_attempts'))
    op.create_index('ix_ai_jobs_case_id', 'ai_jobs', ['case_id'])
    op.create_index('ix_ai_jobs_due', 'ai_jobs', ['status', 'available_at'])


def downgrade():
    raise RuntimeError('Reversión automática deshabilitada para conservar trabajos y textos revisados; requiere respaldo y plan')
