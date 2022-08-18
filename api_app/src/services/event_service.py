from typing import Optional

from aiokafka.producer import AIOKafkaProducer


class EventService:
    def __init__(self,kafka_producer: AIOKafkaProducer):
        self.kafka_producer = kafka_producer

    async def send_message(self, topic: str, key: str, value: str):
        key_encoded = bytes(key, encoding="utf-8")
        value_encoded = bytes(value, encoding="utf-8")
        await self.kafka_producer.send(topic, key=key_encoded, value=value_encoded)
