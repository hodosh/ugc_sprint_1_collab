from functools import lru_cache

from fastapi import Depends

from core.config import settings
from db.async_cache_storage import AsyncCacheStorage
from db.async_message_queue import AsyncMessageQueue
from db.kafka import get_kafka_producer
from db.redis import get_redis

from services.event_service import EventService


@lru_cache()
def get_event_service(
        redis: AsyncCacheStorage = Depends(get_redis),
        kafka_producer: AsyncMessageQueue = Depends(get_kafka_producer),
) -> EventService:
    return EventService(redis, kafka_producer)
