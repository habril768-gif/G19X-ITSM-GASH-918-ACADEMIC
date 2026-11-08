"""Configuración compartida de asistencia IA."""
import os


def enabled() -> bool:
    return os.environ.get("AI_ENABLED", "false").lower() in {"true", "1"}
