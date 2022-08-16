import config
from hl_storage_kafka import KafkaStorage
from hl_storage_clickhouse import ClickhouseStorage

BATCH_SEQUENCE = {
    'Kafka': {
        'client': KafkaStorage(connect_param=config.KAFKA_CONNECT),
        'use': True,
    },
    'Clickhouse': {
        'client': ClickhouseStorage(connect_param=config.CLICKHOUSE_CONNECT),
        'use': True
    }
}
