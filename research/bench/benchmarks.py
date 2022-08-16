import config
from hl_storage_kafka import KafkaStorage
from hl_storage_clickhouse import ClickhouseStorage
from hl_storage_null import DevNullStorage

BATCH_SEQUENCE = {
    'Kafka': {
        'storage': 'Kafka',
        'client': KafkaStorage(connect_param=config.KAFKA_CONNECT),
        'use': True,
        'mode': 'single'
    },
    'Clickhouse1': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=config.CLICKHOUSE_CONNECT),
        'use': True,
        'mode': 'single'
    },
    'Clickhouse2': {
        'storage': 'ClickHouse',
        'client': ClickhouseStorage(connect_param=config.CLICKHOUSE_CONNECT),
        'use': True,
        'mode': 'batch'
    },
    'DevNull': {
        'storage': 'Dev/Null/',
        'client': DevNullStorage(),
        'use': True,
        'mode': 'single'
    }
}
