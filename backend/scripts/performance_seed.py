"""Fixture de rendimiento: ejecutar solo dentro del contenedor QA designado."""
import json
import os
import re
import sys


def guard(payload):
    run_id = payload.get('run_id', '')
    if not re.fullmatch(r'[a-z0-9]{8,24}', run_id):
        raise ValueError('RUN_ID')
    expected = {'POSTGRES_DB': 'plurione_test_perf_' + run_id,
                'POSTGRES_USER': 'qa_perf_' + run_id, 'POSTGRES_HOST': 'postgres',
                'AI_ENABLED': 'false', 'MAIL_ENABLED': 'false'}
    if any(os.environ.get(key) != value for key, value in expected.items()):
        raise ValueError('ENTORNO_NO_QA')
    return run_id


def execute(payload):
    run_id = guard(payload)
    from datetime import date
    from sqlalchemy import func, select
    from sqlalchemy.orm import Session
    from app.core.database import get_engine
    from app.core.security import hash_password
    from app.models import AIJob, AuditEvent, Department, Incident, LocalCredential, MailDelivery, Role, User
    from app.api.incidents import IncidentInput
    from app.services.incidents import create_case

    engine = get_engine()
    def count(db, model):
        return db.scalar(select(func.count()).select_from(model))
    try:
        with Session(engine, expire_on_commit=False) as db:
            if payload.get('action') == 'verify':
                users = db.scalars(select(User)).all()
                if len(users) != 10 or {u.email for u in users} != {
                    f'qa-perf-{run_id}-{index}@example.invalid' for index in range(10)}:
                    raise ValueError('CUENTAS_NO_QA')
                total = count(db, Incident)
                created = db.scalar(select(func.count()).select_from(AuditEvent).where(AuditEvent.accion == 'CREADO'))
                edits = db.scalar(select(func.count()).select_from(AuditEvent).where(AuditEvent.accion == 'CONTENIDO_EDITADO'))
                deliveries = count(db, MailDelivery)
                attempts = db.scalar(select(func.coalesce(func.sum(MailDelivery.attempts), 0)))
                jobs = count(db, AIJob)
                if created != total or deliveries != total * 10 or attempts != 0 or jobs != 0:
                    raise ValueError('AUDITORIA_COLAS_INCONSISTENTES')
                return {'incidencias': total, 'eventos_creado': created, 'eventos_editado': edits,
                        'entregas_encoladas': deliveries, 'intentos_smtp': attempts, 'trabajos_ia': jobs}
            if payload.get('action') != 'seed':
                raise ValueError('ACCION')
            if any(count(db, model) for model in (User, Department, Incident, AuditEvent, LocalCredential, MailDelivery, AIJob)):
                raise ValueError('BASE_NO_VACIA')
            passwords = payload.get('passwords', [])
            if len(passwords) != 10 or any(not isinstance(value, str) or len(value) < 12 for value in passwords):
                raise ValueError('PASSWORDS_QA')
            role = db.scalar(select(Role).where(Role.nombre == 'ADMIN_RH'))
            if role is None:
                raise ValueError('MIGRACION_FALTANTE')
            department = Department(nombre='QA-PERF-' + run_id, is_active=True)
            db.add(department)
            db.flush()
            users = []
            for index, password in enumerate(passwords):
                user = User(email=f'qa-perf-{run_id}-{index}@example.invalid',
                            nombre_completo=f'QA PERF {run_id} {index}', rol_id=role.id,
                            departamento_id=department.id, is_active=True)
                db.add(user)
                db.flush()
                db.add(LocalCredential(user_id=user.id, password_hash=hash_password(password)))
                db.add(AuditEvent(affected_user_id=user.id, accion='USUARIO_ACTUALIZADO',
                                  detalle={'origen': 'QA_PERFORMANCE_FIXTURE'}))
                users.append(user)
            db.commit()
            accounts = []
            for index, user in enumerate(users):
                ids = []
                for offset in range(10):
                    receipt = create_case(db, user, IncidentInput(
                        titulo=f'QA-PERF-{run_id}-inicial-{index}-{offset}',
                        descripcion='Caso ficticio de rendimiento; sin datos personales.',
                        incident_date=date.fromisoformat(payload['incident_date']),
                        scope='ENTORNO', reported_department_id=department.id))
                    ids.append(str(receipt['id']))
                accounts.append({'email': user.email, 'password_env': f'PLURIONE_PERF_PASSWORD_{index}',
                                 'case_ids': ids})
            if count(db, Incident) != 100:
                raise ValueError('CONTEO_INICIAL')
            return {'department_id': str(department.id), 'users': accounts}
    finally:
        engine.dispose()


if __name__ == '__main__':
    try:
        result = execute(json.load(sys.stdin))
        print(json.dumps(result))
    except Exception:
        # No imprimir entrada, credenciales o excepciones del servidor.
        print(json.dumps({'error': 'FIXTURE_QA_RECHAZADO'}))
        raise SystemExit(1)
