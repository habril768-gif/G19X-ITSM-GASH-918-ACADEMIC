from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import UUID, uuid4
import pytest
from sqlalchemy import event, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.ai.contracts import TransientAIError
from app.core.security import utcnow
from app.models import AIJob, AuditEvent, Incident
from app.services.ai import process_one
from test_incidents import world, create, confidential

RESULT = {'result': 'CLASIFICADA', 'category_id': 2, 'priority': 2, 'suggestion': 'Revisar el hecho simulado.', 'reason': 'Situación de conflicto.'}


@pytest.fixture
def setup(world, monkeypatch):
    c, db, a, selected, one, two = world
    monkeypatch.setenv('AI_ENABLED', 'true'); monkeypatch.setenv('OPENAI_MODEL', 'fixture-model')
    monkeypatch.setattr('app.services.ai.notify', lambda ident: False)
    ident = create(c); selected['user'] = a['admin']
    factory = lambda: Session(db.get_bind(), expire_on_commit=False)
    provider = SimpleNamespace(classify=Mock(return_value=dict(RESULT)))
    return c, db, a, selected, UUID(ident), factory, provider


def request(c, ident, **changes):
    return c.post(f'/incidents/{ident}/ai', json={'ai_input_text': 'Dos colaboradores ficticios discrepan sobre una tarea simulada.',
                  'confirmed_simulated': True, 'confirmed_no_identifiers': True, **changes})


def job(db, ident):
    db.expire_all(); return db.scalar(select(AIJob).where(AIJob.case_id == ident).order_by(AIJob.created_at.desc()))


def test_explicit_review_no_original_description_and_durable_idempotence(setup):
    c, db, a, s, ident, factory, provider = setup
    assert request(c, ident, confirmed_simulated=False).status_code == 422
    assert request(c, ident, ai_input_text='Correo ficticio demo@example.invalid').status_code == 422
    r = request(c, ident); assert r.status_code == 202 and r.json()['queue_available'] is False
    first = r.json()['job_id']; assert request(c, ident).json()['job_id'] == first
    row = job(db, ident); assert row.attempts == 0 and row.dispatched_at is None
    assert row.input_text != db.get(Incident, ident).descripcion
    assert row.reviewed_by == a['admin'].id
    provider.classify.assert_not_called()


def test_disabled_or_confidential_never_enqueues_and_manual_remains_available(setup, monkeypatch):
    c, db, a, s, ident, factory, provider = setup
    monkeypatch.setenv('AI_ENABLED', 'false')
    assert request(c, ident).status_code == 503
    assert c.put(f'/incidents/{ident}/classification', json={'category_id': 2, 'priority': 2}).status_code == 200
    monkeypatch.setenv('AI_ENABLED', 'true')
    assert confidential(c, str(ident), True).status_code == 200
    assert request(c, ident).status_code == 409
    assert job(db, ident) is None


def test_employee_and_out_of_scope_supervisor_cannot_review(setup):
    c, db, a, s, ident, factory, provider = setup
    s['user'] = a['employee']; assert request(c, ident).status_code == 403
    assert c.get(f'/incidents/{ident}/ai').status_code == 403
    s['user'] = a['super2']; assert request(c, ident).status_code == 404


def test_success_is_suggestion_only_and_duplicate_worker_does_not_call_again(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    def classify(*args):
        assert process_one(factory, SimpleNamespace(classify=Mock(side_effect=AssertionError('Duplicado')))) is False
        return RESULT
    provider.classify.side_effect = classify
    assert process_one(factory, provider)
    assert process_one(factory, provider) is False
    row = job(db, ident); case = db.get(Incident, ident)
    assert row.status == 'COMPLETADA' and row.attempts == 1 and row.result == RESULT
    assert case.ai_suggestion == RESULT and case.ai_status == 'COMPLETADA'
    assert case.category_id is None and case.priority is None and not case.classification_valid
    status = c.get(f'/incidents/{ident}/ai')
    assert status.headers['cache-control'] == 'no-store' and status.json()['suggestion'] == RESULT
    assert request(c, ident, ai_input_text='Otro texto simulado del mismo hecho.').status_code == 409


def test_abstention_does_not_force_category_or_priority(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    provider.classify.return_value = {'result': 'SIN_CLASIFICACION', 'category_id': None, 'priority': None, 'suggestion': 'Solicitar aclaración.', 'reason': 'Información insuficiente.'}
    assert process_one(factory, provider)
    row = job(db, ident); assert row.status == 'COMPLETADA' and row.result['category_id'] is None
    assert not db.get(Incident, ident).classification_valid


@pytest.mark.parametrize('change', ['privacy', 'role', 'content'])
def test_preflight_cancels_before_external_call(setup, change):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    if change == 'privacy':
        assert confidential(c, str(ident), True).status_code == 200
    elif change == 'role':
        a['admin'].rol_id = 3; db.commit()
    else:
        assert c.put(f'/incidents/{ident}/content', json={'titulo': 'Editado', 'descripcion': 'Otro contenido simulado.'}).status_code == 200
    assert process_one(factory, provider)
    provider.classify.assert_not_called(); row = job(db, ident)
    assert row.status == 'OMITIDA' and row.dispatched_at is None


@pytest.mark.parametrize('change', ['privacy', 'classification', 'content'])
def test_changes_during_request_discard_late_response(setup, change):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    def classify(*args):
        if change == 'privacy':
            assert confidential(c, str(ident), True).status_code == 200
        elif change == 'classification':
            assert c.put(f'/incidents/{ident}/classification', json={'category_id': 4, 'priority': 1}).status_code == 200
        else:
            assert c.put(f'/incidents/{ident}/content', json={'titulo': 'Editado', 'descripcion': 'Nueva descripción simulada.'}).status_code == 200
        return RESULT
    provider.classify.side_effect = classify
    assert process_one(factory, provider)
    row = job(db, ident); case = db.get(Incident, ident)
    assert row.status == 'OMITIDA' and row.result is None and row.dispatched_at is not None
    assert case.ai_suggestion is None
    if change == 'classification': assert case.category_id == 4 and case.priority == 1 and case.classification_valid
    if change == 'content': assert case.content_revision == 1 and case.ai_input_reviewed_at is None


def test_three_transient_attempts_stop_without_raw_error_or_human_change(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident); provider.classify.side_effect = TransientAIError('fixture-secret-must-not-persist')
    for attempt in range(1, 4):
        assert process_one(factory, provider)
        row = job(db, ident); assert row.attempts == attempt
        if attempt < 3:
            assert row.status == 'PENDIENTE'
            assert process_one(factory, provider) is False
            row.available_at = utcnow() - timedelta(seconds=1); db.commit()
    row = job(db, ident); assert row.status == 'FALLIDA' and 'fixture-secret' not in row.error
    assert provider.classify.call_count == 3 and process_one(factory, provider) is False
    assert not db.get(Incident, ident).classification_valid


@pytest.mark.parametrize('result', [dict(RESULT, category_id=999), dict(RESULT, priority=0), dict(RESULT, extra='unexpected')])
def test_bad_schema_or_catalog_fails_without_retry(setup, result):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident); provider.classify.return_value = result
    assert process_one(factory, provider)
    assert job(db, ident).status == 'FALLIDA' and provider.classify.call_count == 1


def test_expired_worker_is_reclaimed_with_attempt_bound(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident); row = job(db, ident)
    row.status = 'EN_PROCESO'; row.attempts = 2; row.lease_token = uuid4(); row.lease_until = utcnow() - timedelta(seconds=1); db.commit()
    provider.classify.side_effect = TransientAIError('Temporal')
    assert process_one(factory, provider)
    row = job(db, ident); assert row.attempts == 3 and row.status == 'FALLIDA'


def test_description_edit_requires_fresh_review_version(setup):
    c, db, a, s, ident, factory, provider = setup
    old = request(c, ident).json()['job_id']
    assert c.put(f'/incidents/{ident}/content', json={'titulo': 'Editado', 'descripcion': 'Nueva versión ficticia.'}).status_code == 200
    assert process_one(factory, provider)
    new = request(c, ident).json()['job_id']; assert new != old
    assert process_one(factory, provider)
    assert job(db, ident).content_revision == 1


def test_expired_attempt_cannot_overwrite_result_saved_by_new_owner(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    newer = dict(RESULT, category_id=4, priority=3)
    def classify(*args):
        with factory() as session:
            row = session.scalar(select(AIJob).where(AIJob.case_id == ident))
            row.lease_until = utcnow() - timedelta(seconds=1); session.commit()
        assert process_one(factory, SimpleNamespace(classify=Mock(return_value=newer)))
        return RESULT
    provider.classify.side_effect = classify
    assert process_one(factory, provider)
    row = job(db, ident)
    assert row.result == newer and row.attempts == 2
    assert db.get(Incident, ident).ai_suggestion == newer


def test_enqueue_audit_failure_rolls_back_job_and_review(setup, monkeypatch):
    c, db, a, s, ident, factory, provider = setup
    signal = Mock(); monkeypatch.setattr('app.services.ai.notify', signal)
    def fail(session, *_):
        if any(isinstance(row, AuditEvent) and row.detalle.get('operation') == 'IA_ENCOLADA' for row in session.new):
            raise SQLAlchemyError('Fallo QA')
    event.listen(db, 'before_flush', fail)
    try:
        assert request(c, ident).status_code == 503
    finally:
        event.remove(db, 'before_flush', fail)
    assert job(db, ident) is None and db.get(Incident, ident).ai_input_text is None
    signal.assert_not_called()


def test_result_audit_failure_does_not_save_partial_suggestion(setup):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    def fail(session, *_):
        if any(isinstance(row, AuditEvent) and row.detalle.get('operation') == 'IA_RESPUESTA' for row in session.new):
            raise SQLAlchemyError('Fallo QA')
    # Hook global limitado a esta prueba para las sesiones del worker.
    event.listen(Session, 'before_flush', fail)
    try:
        with pytest.raises(SQLAlchemyError): process_one(factory, provider)
    finally:
        event.remove(Session, 'before_flush', fail)
    row = job(db, ident)
    assert row.status == 'EN_PROCESO' and row.result is None
    assert db.get(Incident, ident).ai_suggestion is None
@pytest.mark.parametrize('previous', ['plurione-classify-v1', 'plurione-classify-v2', 'plurione-classify-v3'])
def test_previous_prompt_job_is_omitted_before_external_dispatch(setup, previous):
    c, db, a, s, ident, factory, provider = setup
    request(c, ident)
    row = job(db, ident)
    row.prompt_version = previous; db.commit()
    assert process_one(factory, provider)
    db.expire_all()
    assert job(db, ident).status == 'OMITIDA'
    provider.classify.assert_not_called()
