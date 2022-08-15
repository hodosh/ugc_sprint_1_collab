import json
import typing as t

from kafka import (
    KafkaConsumer as _KafkaConsumer,
    OffsetAndMetadata,
    TopicPartition,
)
from kafka.consumer.fetcher import ConsumerRecord

from . import logger


class KafkaConsumer:
    def __init__(self,
                 bootstrap_servers: str,
                 topic_name: str,
                 group_id: str = None,
                 enable_auto_commit: bool = False,
                 max_poll_records: int = 500,
                 **kwargs):
        self._bootstrap_servers = bootstrap_servers
        self._topic_name = topic_name
        self._enable_auto_commit = enable_auto_commit
        self._group_id = group_id
        self._meta: t.Dict[str, t.Any] = kwargs
        self._config: t.Dict[str, t.Any] = {}
        self._consumer: t.Optional[_KafkaConsumer] = None
        self._max_poll_records = max_poll_records

    @property
    def topic_name(self):
        return self._topic_name

    @topic_name.setter
    def topic_name(self, value):
        logger.info(f'Change topic name to "{value}"')
        self._topic_name = value

    @property
    def config(self):
        if not self._config:
            self._config.update(
                {
                    'bootstrap_servers': self._bootstrap_servers,
                    'enable_auto_commit': self._enable_auto_commit,
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
            # api_version=(2,),
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            **self.config)
        logger.info(f'Kafka consumer is started with options: {self.config}')

        self._consumer = consumer
        return self._consumer

    def list_messages(self, timeout_ms: int = 1000, raw: bool = False) -> t.Generator:
        """
        Метод вычитывает сообщения из топика.
        :param timeout_ms: Таймаут ожидания новых сообщений в Kafka при выполнении запроса poll.
        :type raw: признак того, чтобы возвращать ConsumerRecord (raw) или только значения (value) сообщений.
        По умолчанию False.
        """
        logger.info(f'Start listing messages from topic "{self.topic_name}"')
        while True:
            messages_dict = self.consumer.poll(timeout_ms)
            if not messages_dict:
                logger.info(f'There are no new messages in Kafka topic "{self.topic_name}"')
                break
            for consumer_record_list in messages_dict.values():
                for consumer_record in consumer_record_list:
                    logger.info(f'Got message from offset="{consumer_record.offset}" '
                                f'and partition="{consumer_record.partition}"')
                    yield consumer_record if raw else consumer_record.value

    def subscribe(self, offset: int = None, partition: int = 0):
        """
        Подписка на топик
        :param offset: номер оффсета, с которого начинать читать. Необязательный параметр
        :param partition: номер партиции, с которой начинать читать. По умолчанию 0
        """
        logger.info(f'Describe to topic {self.topic_name}')
        if offset:
            logger.info(f'Set offset={offset} in partition={partition}')
            self._specify_offset(offset, partition)
            return
        self.consumer.subscribe([self.topic_name])

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

    def _specify_offset(self, offset: int, partition: int):
        """
        Метод определяет оффсет, с которым необходимо работать, по его номеру и партиции
        """
        tp = TopicPartition(topic=self.topic_name, partition=partition)
        self.consumer.assign([tp])
        self.consumer.seek(tp, offset)

    def close(self):
        """
        Метод закрывает соединение консьюмера с kafka
        """
        logger.info('Close Kafka consumer')
        self.consumer.close()
        self._consumer = None
