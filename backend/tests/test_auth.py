from datetime import timedelta
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.api.auth import PasswordChange, change_password, sign_out
from app.core.security import admin_user, current_user, hash_password, login, token_digest, utcnow
from app.models import AuthSession, Base, Department, LocalCredential, LoginThrottle, Role, User

PASSWORD = "OnlyForTests-LongPassword42"

@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add_all([Role(id=1,nombre="ADMIN_RH"),Role(id=2,nombre="SUPERVISOR"),Role(id=3,nombre="EMPLEADO")])
        dep = Department(nombre="Pruebas", is_active=True)
        db.add(dep); db.flush()
        user = User(email="user@example.invalid", nombre_completo="QA", departamento_id=dep.id, rol_id=3, is_active=True)
        db.add(user); db.flush()
        db.add(LocalCredential(user_id=user.id, password_hash=hash_password(PASSWORD)))
        db.commit()
        yield db
    engine.dispose()

def credentials(token):
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

def test_hash_and_session(db):
    encoded = db.scalar(select(LocalCredential.password_hash))
    assert encoded.startswith("$argon2id$") and PASSWORD not in encoded
    token = login(db, " USER@example.invalid ", PASSWORD)
    assert db.get(AuthSession, token_digest(token)).token_hash != token
    assert current_user(credentials(token), db).email == "user@example.invalid"

def test_wrong_and_unknown_same_error(db):
    errors=[]
    for email in ["user@example.invalid","unknown@example.invalid"]:
        with pytest.raises(HTTPException) as exc: login(db,email,"incorrect")
        errors.append((exc.value.status_code,exc.value.detail))
    assert errors[0] == errors[1]
    assert not db.scalars(select(AuthSession)).all()

def test_lockout(db):
    for _ in range(5):
        with pytest.raises(HTTPException): login(db,"user@example.invalid","incorrect")
    with pytest.raises(HTTPException): login(db,"user@example.invalid",PASSWORD)
    db.get(LoginThrottle,"user@example.invalid").locked_until=utcnow()-timedelta(seconds=1)
    db.commit()
    assert login(db,"user@example.invalid",PASSWORD)

def test_logout_expiry_and_deactivation(db):
    token=login(db,"user@example.invalid",PASSWORD)
    user=current_user(credentials(token),db)
    sign_out(user=user,credentials=credentials(token),db=db)
    with pytest.raises(HTTPException): current_user(credentials(token),db)
    token=login(db,"user@example.invalid",PASSWORD)
    db.get(AuthSession,token_digest(token)).expires_at=utcnow()-timedelta(seconds=1)
    db.commit()
    with pytest.raises(HTTPException): current_user(credentials(token),db)
    token=login(db,"user@example.invalid",PASSWORD)
    user.is_active=False; db.commit()
    with pytest.raises(HTTPException) as exc: current_user(credentials(token),db)
    assert exc.value.status_code==403
    with pytest.raises(HTTPException): login(db,"user@example.invalid",PASSWORD)

def test_employee_cannot_admin(db):
    with pytest.raises(HTTPException) as exc: admin_user(user=db.scalar(select(User)),db=db)
    assert exc.value.status_code==403

def test_password_change_revokes_sessions(db):
    tokens=[login(db,"user@example.invalid",PASSWORD) for _ in range(2)]
    user=current_user(credentials(tokens[0]),db)
    change_password(PasswordChange(current_password=PASSWORD,new_password="New-Password-ForTests42"),user=user,db=db)
    for token in tokens:
        with pytest.raises(HTTPException): current_user(credentials(token),db)
    with pytest.raises(HTTPException): login(db,"user@example.invalid",PASSWORD)
    assert login(db,"user@example.invalid","New-Password-ForTests42")

def test_password_policy():
    for value in ["short"," "*15]:
        with pytest.raises(ValueError): hash_password(value)


def test_http_login_me_logout_and_secret_redaction(db):
    from fastapi.testclient import TestClient
    from app.main import create_app
    from app.core.database import get_session
    app = create_app()
    def test_session():
        yield db
    app.dependency_overrides[get_session] = test_session
    with TestClient(app) as client:
        assert client.get("/auth/me").status_code == 401
        bad = client.post("/auth/login", json={"email":"user@example.invalid", "password":"secret-do-not-echo"*20})
        assert bad.status_code == 422
        assert "secret-do-not-echo" not in bad.text
        response = client.post("/auth/login", json={"email":"user@example.invalid", "password":PASSWORD})
        assert response.status_code == 200
        assert response.headers["cache-control"] == "no-store"
        headers = {"Authorization":"Bearer " + response.json()["access_token"]}
        assert client.get("/auth/me", headers=headers).json()["rol"] == "EMPLEADO"
        assert client.post("/users", headers=headers, json={"email":"new@example.invalid", "password":PASSWORD, "nombre_completo":"QA", "rol_id":3, "departamento_id":str(db.scalar(select(User.departamento_id)))}).status_code == 403
        assert client.post("/auth/logout", headers=headers).status_code == 204
        assert client.get("/auth/me", headers=headers).status_code == 401


def test_admin_creates_user_without_exposing_hash(db):
    from app.api.auth import CreateUser, create_user
    from app.models import AuditEvent
    admin=db.scalar(select(User))
    admin.rol_id=1
    db.commit()
    body=CreateUser(email="new@example.invalid", password=PASSWORD, nombre_completo="QA", rol_id=3, departamento_id=admin.departamento_id)
    result=create_user(body,admin=admin,db=db)
    assert result["rol"] == "EMPLEADO"
    assert "password" not in str(result)
    assert db.scalar(select(AuditEvent)) is not None
    with pytest.raises(HTTPException) as exc:
        create_user(body,admin=admin,db=db)
    assert exc.value.status_code == 409
