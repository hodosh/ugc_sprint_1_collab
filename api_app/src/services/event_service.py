from typing import Optional

from aioredis import Redis
from aiokafka.producer import AIOKafkaProducer

from db.redis_service import RedisService
from models.models import ORJSONModel


class EventService:
    def __init__(self, redis: Redis, kafka_producer: AIOKafkaProducer):
        pass

    async def send_message(self, topic: str, key: str, value: str) -> Optional[ORJSONModel]:
        print('send message')
