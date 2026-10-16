"""Comprobación de disponibilidad del proceso HTTP, sin servicios externos."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Sistema"])


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["plurione-api"]


@router.get("/health", response_model=HealthResponse, summary="Disponibilidad de la API")
async def health() -> HealthResponse:
    """Confirma que la API responde; no comprueba PostgreSQL, Redis ni IA."""
    return HealthResponse(status="ok", service="plurione-api")
