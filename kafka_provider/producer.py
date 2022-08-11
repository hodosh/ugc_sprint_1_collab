import json
import typing as t

from kafka_provider import logger


from kafka import KafkaProducer as _KafkaProducer

from kafka_provider.constants import BOOTSTRAP_SERVERS_KEY


class KafkaProducer:
    def __init__(self,
                 bootstrap_servers: str,
                 topic_name: str,
                 **kwargs):
        self._bootstrap_servers = bootstrap_servers
        self._topic_name = topic_name
        self._meta: t.Dict[str, t.Any] = kwargs
        self._config: t.Dict[str, t.Any] = {}
        self._producer: t.Optional[_KafkaProducer] = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

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
                    BOOTSTRAP_SERVERS_KEY: self._bootstrap_servers,
                    **self._meta,
                },
            )
        return self._config

    @property
    def producer(self) -> _KafkaProducer:
        if self._producer:
            return self._producer

        producer: _KafkaProducer = _KafkaProducer(
            api_version=(2,),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            **self.config)
        logger.info(f'Kafka producer is started with options: {self.config}')

        self._producer = producer
        return self._producer

    @classmethod
    def _on_send_success(cls, record_metadata):
        logger.info(f'Successfully sent to topic "{record_metadata.topic}", '
                    f'partition={record_metadata.partition}, '
                    f'offset={record_metadata.offset}')

    @classmethod
    def _on_send_error(cls, exc):
        logger.error('Send to Kafka caused exception:', exc_info=exc)

    def send_message(self, message: t.Dict[t.Any, t.Any], partition: int = None):
        """
        Отправка сообщения в kafka
        :param partition: номер партиции
        :param message: сообщение в виде словаря
        """
        logger.info(f'Send to Kafka topic `{self.topic_name}`, message:\n{json.dumps(message, indent=4)}\n')
        self.producer.send(topic=self.topic_name,
                           value=message,
                           partition=partition).add_callback(self._on_send_success).add_errback(self._on_send_error)
        self.producer.flush()

    def close(self):
        """
        Метод закрывает соединение продюсера с kafka
        """
        logger.info('Close Kafka producer')
        self.producer.close()
        self._producer = None
