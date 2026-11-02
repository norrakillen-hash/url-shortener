import redis.asyncio as redis
from app.config import settings

# Создаем пул соединений
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
