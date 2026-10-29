"""Proveedor oficial; sin herramientas, trazas externas ni reintentos ocultos."""
from pydantic import ValidationError
from app.ai.contracts import AIResult, PermanentAIError, TransientAIError
from app.ai.prompts import build_instruction


class OpenAIClassifier:
    def __init__(self, api_key):
        self._api_key = api_key

    def classify(self, text, catalog, model, *, metadata_sink=None):
        from langchain_openai import ChatOpenAI
        from langsmith import tracing_context
        from openai import APIConnectionError, APIStatusError, RateLimitError
        try:
            llm = ChatOpenAI(model=model, api_key=self._api_key, base_url='https://api.openai.com/v1',
                             use_responses_api=True, store=False, timeout=30, max_retries=0, max_tokens=1500)
            options = {'include_raw': True} if metadata_sink is not None else {}
            structured = llm.with_structured_output(AIResult, method='json_schema', strict=True, **options)
            instruction = build_instruction(catalog)
            with tracing_context(enabled=False):
                result = structured.invoke([('system', instruction), ('human', text)], config={'callbacks': []})
            if metadata_sink is not None:
                raw = result.get('raw')
                response_metadata = getattr(raw, 'response_metadata', {}) or {}
                usage = getattr(raw, 'usage_metadata', {}) or {}
                metadata_sink.update(
                    response_id=response_metadata.get('id') or getattr(raw, 'id', None),
                    effective_model=response_metadata.get('model_name') or response_metadata.get('model'),
                    usage={key: usage[key] for key in ('input_tokens', 'output_tokens', 'total_tokens')
                           if type(usage.get(key)) is int})
                if result.get('parsing_error') or result.get('parsed') is None:
                    raise PermanentAIError('Respuesta estructurada no válida o rechazada')
                result = result['parsed']
            return AIResult.model_validate(result).model_dump()
        except (APIConnectionError, RateLimitError) as exc:
            raise TransientAIError('Proveedor temporalmente no disponible') from None
        except APIStatusError as exc:
            if exc.status_code >= 500:
                raise TransientAIError('Proveedor temporalmente no disponible') from None
            raise PermanentAIError('El proveedor no pudo completar la clasificación') from None
        except (ValidationError, ValueError):
            raise PermanentAIError('Respuesta estructurada no válida o rechazada') from None
