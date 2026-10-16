"""Ámbitos, revalidación, participantes e IA omitida; conserva filas existentes."""
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("ALTER TABLE incidencias ADD COLUMN scope VARCHAR(10) DEFAULT 'PERSONA' NOT NULL")
    op.execute('ALTER TABLE incidencias ADD COLUMN reported_department_id UUID REFERENCES departamentos(id)')
    op.execute('UPDATE incidencias SET reported_department_id = department_id_at_creation')
    op.execute('ALTER TABLE incidencias ALTER COLUMN reported_department_id SET NOT NULL')
    op.execute('ALTER TABLE incidencias ALTER COLUMN affected_employee_id DROP NOT NULL')
    op.execute('ALTER TABLE incidencias ADD COLUMN classification_valid BOOLEAN DEFAULT false NOT NULL')
    op.execute('UPDATE incidencias SET classification_valid = true WHERE validated_by IS NOT NULL AND validated_at IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_input_text TEXT')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_input_reviewed_by UUID REFERENCES users(id)')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_input_reviewed_at TIMESTAMP WITH TIME ZONE')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_skip_reason TEXT')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_model VARCHAR(120)')
    op.execute('ALTER TABLE incidencias ADD COLUMN ai_prompt_version VARCHAR(80)')
    op.execute('ALTER TABLE incidencias DROP CONSTRAINT ck_incident_ai_status')
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_affected_scope CHECK ((scope = 'PERSONA' AND affected_employee_id IS NOT NULL) OR (scope = 'ENTORNO' AND affected_employee_id IS NULL))")
    op.execute('ALTER TABLE incidencias ADD CONSTRAINT ck_incident_ai_review CHECK ((ai_input_reviewed_by IS NULL AND ai_input_reviewed_at IS NULL) OR (ai_input_reviewed_by IS NOT NULL AND ai_input_reviewed_at IS NOT NULL AND ai_input_text IS NOT NULL AND length(trim(ai_input_text)) > 0))')
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_ai_skip CHECK (ai_status != 'OMITIDA' OR (ai_skip_reason IS NOT NULL AND length(trim(ai_skip_reason)) > 0))")
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_ai_status CHECK (ai_status IN ('PENDIENTE','COMPLETADA','FALLIDA','OMITIDA'))")
    op.execute('ALTER TABLE incidencias ADD CONSTRAINT ck_incident_classification_valid CHECK (NOT classification_valid OR (validated_by IS NOT NULL AND validated_at IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL))')
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_environment_category CHECK (scope != 'ENTORNO' OR category_id IS NULL OR category_id = 4)")
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_resolved_validation CHECK (status NOT IN ('RESUELTA','CERRADA') OR classification_valid)")
    op.execute("ALTER TABLE incidencias ADD CONSTRAINT ck_incident_scope CHECK (scope IN ('PERSONA','ENTORNO'))")
    op.execute('CREATE INDEX ix_incidencias_reported_department_id ON incidencias (reported_department_id)')
    op.execute("CREATE TABLE incident_involved_users (\n\tincidencia_id UUID NOT NULL, \n\tuser_id UUID NOT NULL, \n\treview_status VARCHAR(20) DEFAULT 'DECLARADO' NOT NULL, \n\tdeclaration_reason TEXT NOT NULL, \n\treviewed_by UUID, \n\treviewed_at TIMESTAMP WITH TIME ZONE, \n\treview_reason TEXT, \n\tPRIMARY KEY (incidencia_id, user_id), \n\tCONSTRAINT ck_participant_status CHECK (review_status IN ('DECLARADO','CONFIRMADO','DESCARTADO')), \n\tCONSTRAINT ck_participant_declaration CHECK (length(trim(declaration_reason)) > 0), \n\tCONSTRAINT ck_participant_review CHECK ((review_status = 'DECLARADO' AND reviewed_by IS NULL AND reviewed_at IS NULL AND review_reason IS NULL) OR (review_status IN ('CONFIRMADO','DESCARTADO') AND reviewed_by IS NOT NULL AND reviewed_at IS NOT NULL AND review_reason IS NOT NULL AND length(trim(review_reason)) > 0)), \n\tCONSTRAINT ck_participant_no_self_review CHECK (reviewed_by IS NULL OR reviewed_by != user_id), \n\tFOREIGN KEY(incidencia_id) REFERENCES incidencias (id), \n\tFOREIGN KEY(user_id) REFERENCES users (id), \n\tFOREIGN KEY(reviewed_by) REFERENCES users (id)\n)")
    op.execute('CREATE INDEX ix_incident_involved_users_user_id ON incident_involved_users (user_id)')

def downgrade():
    raise RuntimeError("Reversión automática deshabilitada: preservar casos ENTORNO, participantes y evidencia de validación; requiere respaldo y plan explícito")
