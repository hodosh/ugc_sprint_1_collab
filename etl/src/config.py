from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_brokers = Field(env='KAFKA_BROKERS', default='127.0.0.1:29092')
    kafka_topics = Field(env='KAFKA_TOPICS', default='events_topic')
    kafka_group_id: str = Field(env='KAFKA_GROUP_ID', default='my-group')
    kafka_poll_timeout_ms: str = Field(env='KAFKA_POLL_TIMEOUT_MS', default=3000)
    clickhouse_host = Field(env='CLICKHOUSE_HOST', default='127.0.0.1')
    clickhouse_database = Field(env='CLICKHOUSE_DATABASE', default='events')
    clickhouse_table = Field(env='CLICKHOUSE_TABLE', default='events')
    clickhouse_cluster = Field(env='CLICKHOUSE_CLUSTER', default='company_cluster')
    etl_batch_size = Field(env='BATCH_SIZE', default=500)
    etl_pause_duration = Field(env='PAUSE_DURATION', default=30)


settings = Settings()
