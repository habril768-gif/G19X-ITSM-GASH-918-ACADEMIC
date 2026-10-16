"""Comprobación de disponibilidad del proceso HTTP, sin servicios externos."""

from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.core.database import database_ready
from pydantic import BaseModel

router = APIRouter(tags=["Sistema"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["plurione-api"]


@router.get("/health", response_model=HealthResponse, summary="Disponibilidad de la API")
async def health() -> HealthResponse:
    """Confirma que la API responde; no comprueba PostgreSQL, Redis ni IA."""
    return HealthResponse(status="ok", service="plurione-api")


@router.get("/health/db", summary="Disponibilidad de PostgreSQL y migración", responses={503: {"description": "Base de datos no disponible o sin migrar"}})
def health_database(ready: bool = Depends(database_ready)):
    return JSONResponse(
        status_code=200 if ready else 503,
        content={"status": "ok" if ready else "unavailable", "database": "postgresql"},
    )
