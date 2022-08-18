import time
from contextlib import closing

from config import settings
from services.clickhouse_loader import ClickHouseLoader
from services.kafka_extractor import KafkaExtractor
from utils import backoff


@backoff()
def run():
    with closing(ClickHouseLoader(host=settings.clickhouse_host,
                                  database=settings.clickhouse_database,
                                  table=settings.clickhouse_film_view_table,
                                  cluster=settings.clickhouse_cluster,
                                  batch_size=settings.etl_batch_size)) as clickhouse, closing(
        KafkaExtractor(bootstrap_servers=settings.kafka_brokers,
                       topic_list=settings.kafka_topics,
                       group_id=settings.kafka_group_id,
                       batch_size=settings.etl_batch_size)) as kafka:
        # subscribe to topic
        kafka.subscribe()
        # init database
        clickhouse.create_database()
        clickhouse.create_table()
        input_data_gen = kafka.list_messages()
        if input_data_gen:
            clickhouse.load(data=input_data_gen)


if __name__ == '__main__':
    while True:
        run()
        time.sleep(settings.etl_pause_duration)
