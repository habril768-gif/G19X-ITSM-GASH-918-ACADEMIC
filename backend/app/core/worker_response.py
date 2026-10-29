"""Prepara y valida DTOs en el worker que ejecuta el endpoint síncrono."""
from functools import wraps

from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool


def worker_response(model):
    """Conserva firma y response_model; devuelve al loop solo un DTO validado."""
    def decorate(function):
        def _run_validated_endpoint(*args, **kwargs):
            result = function(*args, **kwargs)
            try:
                return model.model_validate(result)
            except ValidationError as error:
                errors = [dict(item, loc=('response', *item['loc'])) for item in error.errors()]
                raise ResponseValidationError(errors, body=result) from None

        def bind(worker):
            @wraps(function)
            async def endpoint(*args, **kwargs):
                return await run_in_threadpool(worker, *args, **kwargs)

            # Permite al diagnóstico envolver el trabajo síncrono, sin incluir
            # espera/retorno en su métrica endpoint ni volver síncrona la ruta.
            endpoint.response_worker = worker
            endpoint.with_response_worker = bind
            return endpoint

        return bind(_run_validated_endpoint)
    return decorate
