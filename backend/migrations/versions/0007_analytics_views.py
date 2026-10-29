"""Vistas agregadas con supresión en origen, sin filas personales exportables."""
from pathlib import Path
from alembic import op
revision='0007'
down_revision='0006'
branch_labels=None
depends_on=None

def upgrade():
    source=Path(__file__).with_suffix('.sql').read_text(encoding='utf-8')
    for statement in source.split('-- statement\n'):
        if statement.strip(): op.execute(statement)

def downgrade():
    raise RuntimeError('Reversión de analítica requiere revisar credenciales y copias entregadas')
