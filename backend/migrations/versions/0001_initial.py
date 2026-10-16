"""Esquema y catálogos iniciales. DDL congelado para PostgreSQL."""
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute('CREATE TABLE categorias_incidencia (\n\tid SERIAL NOT NULL, \n\tnombre VARCHAR(80) NOT NULL, \n\tdescripcion TEXT NOT NULL, \n\tPRIMARY KEY (id), \n\tUNIQUE (nombre)\n)')
    op.execute("CREATE TABLE departamentos (\n\tid UUID NOT NULL, \n\tnombre VARCHAR(120) NOT NULL, \n\tis_active BOOLEAN DEFAULT 'true' NOT NULL, \n\tPRIMARY KEY (id), \n\tUNIQUE (nombre)\n)")
    op.execute('CREATE TABLE roles (\n\tid SERIAL NOT NULL, \n\tnombre VARCHAR(30) NOT NULL, \n\tPRIMARY KEY (id), \n\tUNIQUE (nombre)\n)')
    op.execute("CREATE TABLE users (\n\tid UUID NOT NULL, \n\temail VARCHAR(320) NOT NULL, \n\texternal_id UUID NOT NULL, \n\ttenant_id UUID NOT NULL, \n\tnombre_completo VARCHAR(200) NOT NULL, \n\tdepartamento_id UUID NOT NULL, \n\trol_id INTEGER NOT NULL, \n\tis_active BOOLEAN DEFAULT 'true' NOT NULL, \n\tPRIMARY KEY (id), \n\tCONSTRAINT uq_users_entra UNIQUE (tenant_id, external_id), \n\tFOREIGN KEY(departamento_id) REFERENCES departamentos (id), \n\tFOREIGN KEY(rol_id) REFERENCES roles (id)\n)")
    op.execute('CREATE INDEX ix_users_departamento_id ON users (departamento_id)')
    op.execute("CREATE TABLE incidencias (\n\tid UUID NOT NULL, \n\ttitulo VARCHAR(200) NOT NULL, \n\tdescripcion TEXT NOT NULL, \n\tincident_date DATE NOT NULL, \n\tcreated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tupdated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tstatus VARCHAR(20) DEFAULT 'PENDIENTE' NOT NULL, \n\tpriority INTEGER, \n\tcategory_id INTEGER, \n\tai_suggestion JSONB, \n\tai_error TEXT, \n\tai_status VARCHAR(20) DEFAULT 'PENDIENTE' NOT NULL, \n\tvalidated_by UUID, \n\tvalidated_at TIMESTAMP WITH TIME ZONE, \n\tresolution_text TEXT, \n\tresolved_at TIMESTAMP WITH TIME ZONE, \n\tclosed_at TIMESTAMP WITH TIME ZONE, \n\tcycle_start_at TIMESTAMP WITH TIME ZONE, \n\treopening_reason TEXT, \n\tis_confidential BOOLEAN DEFAULT 'false' NOT NULL, \n\tcreated_by UUID NOT NULL, \n\taffected_employee_id UUID NOT NULL, \n\tassigned_to UUID, \n\tdepartment_id_at_creation UUID NOT NULL, \n\tPRIMARY KEY (id), \n\tCONSTRAINT ck_incident_status CHECK (status IN ('PENDIENTE','EN_REVISION','RESUELTA','CERRADA')), \n\tCONSTRAINT ck_incident_priority CHECK (priority IS NULL OR priority IN (1,2,3)), \n\tCONSTRAINT ck_incident_ai_status CHECK (ai_status IN ('PENDIENTE','COMPLETADA','FALLIDA')), \n\tCONSTRAINT ck_incident_assigned CHECK (status = 'PENDIENTE' OR (assigned_to IS NOT NULL AND category_id IS NOT NULL AND priority IS NOT NULL AND cycle_start_at IS NOT NULL)), \n\tCONSTRAINT ck_incident_resolution CHECK (status NOT IN ('RESUELTA','CERRADA') OR (resolved_at IS NOT NULL AND length(trim(resolution_text)) > 0 AND resolution_text IS NOT NULL AND validated_by IS NOT NULL AND validated_at IS NOT NULL)), \n\tCONSTRAINT ck_incident_closed CHECK (status != 'CERRADA' OR closed_at IS NOT NULL), \n\tFOREIGN KEY(category_id) REFERENCES categorias_incidencia (id), \n\tFOREIGN KEY(validated_by) REFERENCES users (id), \n\tFOREIGN KEY(created_by) REFERENCES users (id), \n\tFOREIGN KEY(affected_employee_id) REFERENCES users (id), \n\tFOREIGN KEY(assigned_to) REFERENCES users (id), \n\tFOREIGN KEY(department_id_at_creation) REFERENCES departamentos (id)\n)")
    op.execute('CREATE INDEX ix_incidencias_affected_employee_id ON incidencias (affected_employee_id)')
    op.execute('CREATE INDEX ix_incidencias_assigned_to ON incidencias (assigned_to)')
    op.execute('CREATE INDEX ix_incidencias_created_by ON incidencias (created_by)')
    op.execute('CREATE INDEX ix_incident_status_priority ON incidencias (status, priority)')
    op.execute("CREATE TABLE historial_incidencias (\n\tid UUID NOT NULL, \n\tincidencia_id UUID, \n\taffected_user_id UUID, \n\tusuario_id UUID, \n\taccion VARCHAR(40) NOT NULL, \n\tdetalle JSONB NOT NULL, \n\tfecha TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, \n\tPRIMARY KEY (id), \n\tCONSTRAINT ck_audit_action CHECK (accion IN ('CREADO','ESTADO_CAMBIADO','ASIGNADO','REAPERTURA','VALIDACION_IA','CAMBIO_CONFIDENCIALIDAD','CONTENIDO_EDITADO','USUARIO_ACTUALIZADO')), \n\tCONSTRAINT ck_audit_target CHECK (incidencia_id IS NOT NULL OR affected_user_id IS NOT NULL), \n\tFOREIGN KEY(incidencia_id) REFERENCES incidencias (id), \n\tFOREIGN KEY(affected_user_id) REFERENCES users (id), \n\tFOREIGN KEY(usuario_id) REFERENCES users (id)\n)")
    op.execute('CREATE INDEX ix_historial_incidencias_incidencia_id ON historial_incidencias (incidencia_id)')
    op.execute("INSERT INTO roles (id, nombre) VALUES (1, 'ADMIN_RH'), (2, 'SUPERVISOR'), (3, 'EMPLEADO')")
    op.execute("INSERT INTO categorias_incidencia (id, nombre, descripcion) VALUES (1,'Ausencias','Faltas, retardos y permisos no autorizados'), (2,'Conflictos','Problemas interpersonales'), (3,'Incumplimientos','Violaciones de politicas internas'), (4,'Riesgos','Condiciones inseguras'), (5,'Solicitudes Administrativas','Tramites con seguimiento RH')")

def downgrade():
    op.drop_table('historial_incidencias')
    op.drop_table('incidencias')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('departamentos')
    op.drop_table('categorias_incidencia')
