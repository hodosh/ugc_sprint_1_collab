from typing import Optional

from aiokafka.producer import AIOKafkaProducer
from models.models import EventMessage

class EventService:
    def __init__(self,kafka_producer: AIOKafkaProducer):
        self.kafka_producer = kafka_producer

    async def send_message(self, event_message:EventMessage ):
        key_encoded = bytes(str(event_message.key), encoding="utf-8")
        value_encoded = bytes(str(event_message.value), encoding="utf-8")
        await self.kafka_producer.send(event_message.topic, key=key_encoded, value=value_encoded)
