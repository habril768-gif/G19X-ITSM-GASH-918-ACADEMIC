import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PROMPT_VERSION = 'plurione-classify-v1'


class AIInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    ai_input_text: str = Field(min_length=1, max_length=4000)
    confirmed_simulated: Literal[True]
    confirmed_no_identifiers: Literal[True]

    @field_validator('ai_input_text')
    @classmethod
    def reviewed_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError('Escribe texto simulado revisado')
        if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|https?://|\b[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,}\b', value):
            raise ValueError('Retira correos, enlaces e identificadores del texto')
        return value


class AIResult(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    result: Literal['CLASIFICADA', 'SIN_CLASIFICACION']
    category_id: int | None = Field(ge=1)
    priority: int | None = Field(ge=1, le=3)
    suggestion: str = Field(min_length=1, max_length=1000)
    reason: str = Field(min_length=1, max_length=1000)

    @field_validator('suggestion', 'reason')
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError('Salida vacía')
        return value.strip()

    @model_validator(mode='after')
    def coherent(self):
        has_labels = self.category_id is not None and self.priority is not None
        if self.result == 'CLASIFICADA' and not has_labels:
            raise ValueError('Clasificación incompleta')
        if self.result == 'SIN_CLASIFICACION' and (self.category_id is not None or self.priority is not None):
            raise ValueError('La abstención no lleva categoría ni prioridad')
        return self


class TransientAIError(Exception):
    pass


class PermanentAIError(Exception):
    pass
