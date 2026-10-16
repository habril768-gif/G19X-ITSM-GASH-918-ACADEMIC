"""Punto de entrada ASGI de PluriOne."""

from fastapi import FastAPI

from app.api.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="PluriOne API",
        version="0.2.0",
        description=(
            "API de Gestión de Incidencias Laborales. "
            "Disponibilidad del proceso y conexión PostgreSQL con esquema versionado."
        ),
    )
    app.include_router(health_router)
    return app


app = create_app()
