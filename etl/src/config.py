from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_brokers = Field(env='KAFKA_BROKERS', default='localhost:9092')
    kafka_topics = Field(env='KAFKA_TOPICS', default='events_topic')
    kafka_group_id = Field(env='KAFKA_GROUP_ID', default='group_id_0')
    clickhouse_host = Field(env='CLICKHOUSE_HOST', default='')
    clickhouse_database = Field(env='CLICKHOUSE_DATABASE', default='events')
    clickhouse_table = Field(env='CLICKHOUSE_TABLE', default='events')
    clickhouse_cluster = Field(env='CLICKHOUSE_CLUSTER', default='company_cluster')
    etl_batch_size = Field(env='BATCH_SIZE', default=500)


settings = Settings()
