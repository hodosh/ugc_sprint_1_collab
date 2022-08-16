from clickhouse_driver import Client
from hl_storage_abstract import HiLoadStorage


class ClickhouseStorage(HiLoadStorage):
    def __init__(self, connect_param):
        self.client = Client(host=connect_param)

    def insert(self, data=None):
        query = f"INSERT INTO movies_statistics.view_stat (movie_id, user_id, eventTime, view_run_time) " \
                f"VALUES ('{data.movie_id}', '{data.user_id}', '{data.event_time}', {data.view_run_time})"
        self.client.execute(query)

    def insert_batch(self, data=None, batch_size: int = 10):
        pass
