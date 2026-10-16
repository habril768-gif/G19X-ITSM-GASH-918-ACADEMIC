"""Autenticación local sin eliminar identidades ni incidencias existentes."""
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

def upgrade():
    op.execute('ALTER TABLE users ALTER COLUMN external_id DROP NOT NULL')
    op.execute('ALTER TABLE users ALTER COLUMN tenant_id DROP NOT NULL')
    op.execute('ALTER TABLE users ADD CONSTRAINT ck_users_identity_pair CHECK ((tenant_id IS NULL) = (external_id IS NULL))')
    op.execute('CREATE UNIQUE INDEX uq_users_email_lower ON users (lower(email))')
    op.execute("CREATE TABLE login_throttle (\n\temail VARCHAR(320) NOT NULL, \n\tfailures INTEGER DEFAULT '0' NOT NULL, \n\tlocked_until TIMESTAMP WITH TIME ZONE, \n\tPRIMARY KEY (email)\n)")
    op.execute('CREATE TABLE auth_sessions (\n\ttoken_hash VARCHAR(64) NOT NULL, \n\tuser_id UUID NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\texpires_at TIMESTAMP WITH TIME ZONE NOT NULL, \n\trevoked_at TIMESTAMP WITH TIME ZONE, \n\tPRIMARY KEY (token_hash), \n\tFOREIGN KEY(user_id) REFERENCES users (id)\n)')
    op.execute('CREATE INDEX ix_auth_sessions_user_id ON auth_sessions (user_id)')
    op.execute('CREATE TABLE local_credentials (\n\tuser_id UUID NOT NULL, \n\tpassword_hash TEXT NOT NULL, \n\tupdated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tPRIMARY KEY (user_id), \n\tFOREIGN KEY(user_id) REFERENCES users (id)\n)')

def downgrade():
    raise RuntimeError("Reversión automática deshabilitada para preservar credenciales y cuentas locales; requiere plan de migración y respaldo")
