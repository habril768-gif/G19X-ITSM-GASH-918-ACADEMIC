"""Regresión de consulta de sesión agrupada, sin cachear revocación o actividad."""
from datetime import timedelta
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import event, select, update
from sqlalchemy.orm import Session
from app.core.security import current_user, token_digest, utcnow
from app.models import AuthSession, Department, User
from test_auth import db, credentials


def issue(db):
    token = 'SimulatedSessionForQueryTests'
    user = db.scalar(select(User))
    db.add(AuthSession(token_hash=token_digest(token), user_id=user.id,
                       expires_at=utcnow() + timedelta(hours=1)))
    db.commit()
    return token, user.id


def test_valid_session_uses_one_select(db):
    token, user_id = issue(db)
    db.expire_all()
    selects = []
    def observe(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith('SELECT'):
            selects.append(statement)
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        user = current_user(credentials(token), db)
        assert user.id == user_id
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert len(selects) == 1


@pytest.mark.parametrize('change,expected', [
    ('revoked', 401), ('expired', 401), ('inactive_user', 403),
    ('inactive_department', 403), ('expired_inactive', 401), ('unknown', 401),
])
def test_join_preserves_rejection_status_and_challenge(db, change, expected):
    token, user_id = issue(db)
    auth = db.get(AuthSession, token_digest(token))
    user = db.get(User, user_id)
    if change == 'revoked': auth.revoked_at = utcnow()
    if change in {'expired', 'expired_inactive'}: auth.expires_at = utcnow() - timedelta(seconds=1)
    if change in {'inactive_user', 'expired_inactive'}: user.is_active = False
    if change == 'inactive_department': db.get(Department, user.departamento_id).is_active = False
    db.commit()
    with pytest.raises(HTTPException) as caught:
        current_user(credentials('UnknownSimulatedToken' if change == 'unknown' else token), db)
    assert caught.value.status_code == expected
    if expected == 401:
        assert caught.value.detail == 'Sesión inválida o expirada'
        assert caught.value.headers == {'WWW-Authenticate': 'Bearer'}
    else:
        assert caught.value.detail == 'Cuenta no habilitada'


@pytest.mark.parametrize('header', [None,
    HTTPAuthorizationCredentials(scheme='Basic', credentials='simulated'),
    HTTPAuthorizationCredentials(scheme='Bearer', credentials='x' * 257)])
def test_invalid_header_is_rejected_without_sql(db, header):
    statements = []
    def observe(conn, cursor, statement, parameters, context, executemany): statements.append(statement)
    event.listen(db.bind, 'before_cursor_execute', observe)
    try:
        with pytest.raises(HTTPException) as caught:
            current_user(header, db)
    finally:
        event.remove(db.bind, 'before_cursor_execute', observe)
    assert caught.value.status_code == 401
    assert caught.value.detail == 'Sesión requerida'
    assert not statements


@pytest.mark.parametrize('change,expected', [('revoked', 401), ('user', 403), ('department', 403)])
def test_preloaded_identity_does_not_hide_external_revocation_or_deactivation(db, change, expected):
    token, user_id = issue(db)
    user = current_user(credentials(token), db)
    held_session = db.get(AuthSession, token_digest(token))
    held_department = db.get(Department, user.departamento_id)
    assert held_session.revoked_at is None and user.is_active and held_department.is_active
    with Session(db.bind) as other:
        if change == 'revoked':
            other.execute(update(AuthSession).where(AuthSession.token_hash == token_digest(token)).values(revoked_at=utcnow()))
        elif change == 'user':
            other.execute(update(User).where(User.id == user_id).values(is_active=False))
        else:
            other.execute(update(Department).where(Department.id == held_department.id).values(is_active=False))
        other.commit()
    with pytest.raises(HTTPException) as caught:
        current_user(credentials(token), db)
    assert caught.value.status_code == expected
