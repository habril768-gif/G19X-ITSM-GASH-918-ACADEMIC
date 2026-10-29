"""Punto de entrada ASGI de PluriOne."""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.incidents import router as incidents_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.departments import router as departments_router
from app.api.ai import router as ai_router
from app.api.mail import router as mail_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="PluriOne API",
        version="0.12.0",
        description=(
            "API de Gestión de Incidencias Laborales con autenticación local, "
            "gestión de expedientes, auditoría y seguimiento de asistencia IA y correo."
        ),
    )
    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        return JSONResponse(status_code=503, content={"detail": "Servicio de datos temporalmente no disponible"})

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        errors = [{"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
        return JSONResponse(status_code=422, content={"detail": errors})

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(incidents_router)
    app.include_router(users_router)
    app.include_router(departments_router)
    app.include_router(ai_router)
    app.include_router(mail_router)
    return app


app = create_app()
