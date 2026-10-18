"""Redis transporta avisos sin texto; PostgreSQL conserva el trabajo durable."""
import os
from redis import Redis
from redis.exceptions import RedisError

KEY = 'plurione:ai:wakeup'


def client():
    return Redis.from_url(os.environ.get('REDIS_URL', 'redis://redis:6379/0'), decode_responses=True,
                          socket_connect_timeout=1, socket_timeout=6)


def notify(job_id):
    try:
        with client() as redis:
            redis.lpush(KEY, str(job_id)); redis.ltrim(KEY, 0, 999)
        return True
    except (RedisError, ValueError):
        return False


def wait():
    try:
        with client() as redis:
            redis.blpop(KEY, timeout=5)
        return True
    except (RedisError, ValueError):
        return False
