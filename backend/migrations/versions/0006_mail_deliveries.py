"""Outbox de correo por eventos; no genera mensajes retrospectivos."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('mail_deliveries',
        sa.Column('id', sa.Uuid(), primary_key=True),
        sa.Column('event_id', sa.Uuid(), sa.ForeignKey('historial_incidencias.id'), nullable=False),
        sa.Column('case_id', sa.Uuid(), sa.ForeignKey('incidencias.id'), nullable=False),
        sa.Column('recipient_id', sa.Uuid(), sa.ForeignKey('users.id')),
        sa.Column('kind', sa.String(20), nullable=False),
        sa.Column('context', postgresql.JSONB(), nullable=False),
        sa.Column('status', sa.String(20), server_default='PENDIENTE', nullable=False),
        sa.Column('attempts', sa.Integer(), server_default='0', nullable=False),
        sa.Column('available_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('lease_until', sa.DateTime(timezone=True)), sa.Column('lease_token', sa.Uuid()),
        sa.Column('error', sa.String(200)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.UniqueConstraint('event_id', 'recipient_id', name='uq_mail_event_recipient'),
        sa.CheckConstraint("kind IN ('CREACION','ASIGNACION','RESOLUCION','REAPERTURA')", name='ck_mail_kind'),
        sa.CheckConstraint("status IN ('PENDIENTE','EN_PROCESO','ENVIADA','FALLIDA','OMITIDA')", name='ck_mail_status'),
        sa.CheckConstraint('attempts BETWEEN 0 AND 4', name='ck_mail_attempts'))
    op.create_index('ix_mail_deliveries_case_id', 'mail_deliveries', ['case_id'])
    op.create_index('ix_mail_due', 'mail_deliveries', ['status', 'available_at'])

def downgrade():
    raise RuntimeError('Conservar historial de entregas; reversión requiere respaldo y plan explícito')
