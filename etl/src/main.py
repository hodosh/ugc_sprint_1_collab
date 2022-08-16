import time

from config import settings
from services.kafka_extractor import KafkaExtractor
from services.clickhouse_loader import ClickHouseLoader


def run(kafka: KafkaExtractor, clickhouse: ClickHouseLoader):
    while True:
        input_data_gen = kafka.list_messages()
        if input_data_gen:
            # todo transform with pydantic
            transformed_data = input_data_gen
            clickhouse.load(data=transformed_data)
        # пауза между командами
        time.sleep(settings.etl_pause_duration)


if __name__ == '__main__':
    clickhouse = ClickHouseLoader(host=settings.clickhouse_host,
                                  database=settings.clickhouse_database,
                                  table=settings.clickhouse_table,
                                  cluster=settings.clickhouse_cluster,
                                  batch_size=settings.etl_batch_size)

    kafka = KafkaExtractor(bootstrap_servers=settings.kafka_brokers,
                           topic_name=settings.kafka_topics,
                           group_id=settings.kafka_group_id,
                           batch_size=settings.etl_batch_size)
    # subscribe to topic
    kafka.subscribe()
    # init database
    clickhouse.create_table()

    # run etl
    run(kafka=kafka, clickhouse=clickhouse)
