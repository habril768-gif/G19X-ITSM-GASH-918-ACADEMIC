"""Añade aviso de cierre sin modificar ni reenviar entregas históricas."""
from alembic import op

revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('ck_mail_kind', 'mail_deliveries', type_='check')
    op.create_check_constraint('ck_mail_kind', 'mail_deliveries',
        "kind IN ('CREACION','ASIGNACION','RESOLUCION','REAPERTURA','CIERRE')")


def downgrade():
    raise RuntimeError('Conservar avisos de cierre; reversión requiere respaldo y plan explícito')
