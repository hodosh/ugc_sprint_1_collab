import json
import typing as t

from kafka import (
    KafkaConsumer as _KafkaConsumer,
    OffsetAndMetadata,
    TopicPartition,
)
from kafka.consumer.fetcher import ConsumerRecord

from . import logger


class KafkaExtractor:
    def __init__(self,
                 bootstrap_servers: str,
                 topic_name: str,
                 group_id: str = None,
                 batch_size: int = 500,
                 **kwargs):
        self._bootstrap_servers = bootstrap_servers
        self._topic_name = topic_name
        self._group_id = group_id
        self._meta: t.Dict[str, t.Any] = kwargs
        self._config: t.Dict[str, t.Any] = {}
        self._consumer: t.Optional[_KafkaConsumer] = None
        self._max_poll_records = batch_size

    @property
    def config(self):
        if not self._config:
            self._config.update(
                {
                    'bootstrap_servers': self._bootstrap_servers,
                    'group_id': self._group_id,
                    'max_poll_records': self._max_poll_records,
                    **self._meta,
                },
            )
        return self._config

    @property
    def consumer(self) -> _KafkaConsumer:
        if self._consumer:
            return self._consumer

        consumer: _KafkaConsumer = _KafkaConsumer(
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            **self.config)
        logger.info(f'Kafka consumer is started with options: {self.config}')

        self._consumer = consumer
        return self._consumer

    def list_messages(self, timeout_ms: int = 1000) -> t.Generator:
        """
        Метод вычитывает сообщения из топика.
        :param timeout_ms: Таймаут ожидания новых сообщений в Kafka при выполнении запроса poll.
        """
        logger.info(f'Start listing messages from topic "{self._topic_name}"')
        while True:
            messages_dict = self.consumer.poll(timeout_ms)
            if not messages_dict:
                logger.info(f'There are no new messages in Kafka topic "{self._topic_name}"')
                break
            for consumer_record_list in messages_dict.values():
                for consumer_record in consumer_record_list:
                    logger.info(f'Got message from offset="{consumer_record.offset}" '
                                f'and partition="{consumer_record.partition}"')
                    yield consumer_record.value
                    self.commit(consumer_record)

    def subscribe(self):
        """
        Подписка на топик
        """
        logger.info(f'Describe to topic {self._topic_name}')
        self.consumer.subscribe([self._topic_name])

    def commit(self, message: ConsumerRecord):
        """
        Метод для коммита сообщения
        :param message: сообщение типа ConsumerRecord
        """
        logger.info(f'Commit message from offset={message.offset}')
        tp = TopicPartition(message.topic, message.partition)
        meta = self.consumer.partitions_for_topic(message.topic)
        options = {tp: OffsetAndMetadata(message.offset + 1, meta)}
        self.consumer.commit(options)

    def close(self):
        """
        Метод закрывает соединение консьюмера с kafka
        """
        logger.info('Close Kafka consumer')
        self.consumer.close()
        self._consumer = None
