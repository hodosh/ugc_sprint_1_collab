from functools import lru_cache

from fastapi import Depends

from core.config import settings
from db.async_message_queue import AsyncMessageQueue
from db.kafka import get_kafka_producer

from services.event_service import EventService


@lru_cache()
def get_event_service(
        kafka_producer: AsyncMessageQueue = Depends(get_kafka_producer),
) -> EventService:
    return EventService(kafka_producer = kafka_producer)
