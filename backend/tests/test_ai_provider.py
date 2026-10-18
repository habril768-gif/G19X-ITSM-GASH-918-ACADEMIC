from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from redis.exceptions import ConnectionError as RedisConnectionError
from app.ai import queue
from app.ai.provider import OpenAIClassifier
from app.ai.contracts import AIResult, PermanentAIError, TransientAIError
from test_ai import RESULT


def test_langchain_uses_only_reviewed_text_official_endpoint_no_store_and_no_hidden_retry(monkeypatch):
    import langchain_openai
    invoke = Mock(return_value=AIResult(**RESULT)); structured = SimpleNamespace(invoke=invoke)
    llm = SimpleNamespace(with_structured_output=Mock(return_value=structured)); constructor = Mock(return_value=llm)
    monkeypatch.setattr(langchain_openai, 'ChatOpenAI', constructor)
    value = OpenAIClassifier('fixture-key-not-real').classify('Solo texto revisado simulado.', [{'id': 2, 'nombre': 'Conflictos'}], 'fixture-model')
    assert value == RESULT
    config = constructor.call_args.kwargs
    assert config['store'] is False and config['max_retries'] == 0 and config['use_responses_api'] is True
    assert config['max_tokens'] == 1500
    assert config['base_url'] == 'https://api.openai.com/v1'
    messages = invoke.call_args.args[0]; assert messages[1] == ('human', 'Solo texto revisado simulado.')
    assert 'no confiable' in messages[0][1] and 'SIN_CLASIFICACION' in messages[0][1]


def test_redis_signal_contains_only_id_and_failure_keeps_durable_path(monkeypatch):
    redis = Mock(); redis.__enter__ = Mock(return_value=redis); redis.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(queue, 'client', lambda: redis)
    assert queue.notify('fixture-job-id')
    redis.lpush.assert_called_once_with(queue.KEY, 'fixture-job-id')
    redis.lpush.side_effect = RedisConnectionError('fixture-sensitive-detail')
    assert queue.notify('fixture-job-id') is False


def test_real_langchain_openai_adapter_serializes_and_parses_mock_responses_api(monkeypatch):
    import json
    import httpx2
    import langchain_openai
    real_class = langchain_openai.ChatOpenAI; requests = []
    def handler(request):
        requests.append(json.loads(request.content))
        return httpx2.Response(200, json={
            'id': 'resp_fixture', 'object': 'response', 'created_at': 0, 'status': 'completed', 'model': 'fixture-model',
            'output': [{'id': 'msg_fixture', 'type': 'message', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': json.dumps(RESULT), 'annotations': []}]}],
            'usage': {'input_tokens': 10, 'output_tokens': 10, 'total_tokens': 20},
        })
    with httpx2.Client(transport=httpx2.MockTransport(handler)) as transport:
        monkeypatch.setattr(langchain_openai, 'ChatOpenAI', lambda **kwargs: real_class(**kwargs, http_client=transport))
        result = OpenAIClassifier('fixture-no-network').classify('Texto ficticio revisado.', [{'id': 2, 'nombre': 'Conflictos'}], 'fixture-model')
    assert result == RESULT and len(requests) == 1
    assert requests[0]['store'] is False and requests[0]['text']['format']['type'] == 'json_schema'
    assert requests[0]['max_output_tokens'] == 1500
    assert 'Texto ficticio revisado.' in json.dumps(requests[0], ensure_ascii=False)
