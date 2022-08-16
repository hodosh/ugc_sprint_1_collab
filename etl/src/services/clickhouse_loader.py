import typing as t

from clickhouse_driver import Client


class ClickHouseLoader:
    def __init__(self,
                 host: str,
                 database: str,
                 table: str,
                 batch_size: int = 500,
                 cluster: str = 'company_cluster'):
        self._host = host
        self._database = database
        self._table = table
        self._batch_size = batch_size
        self._cluster = cluster
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = Client(host=self._host)

        return self._client

    def load(self, data: t.Generator):
        """
        Метод загружает данные в таблицу
        :param data: словарь данных
        """
        for event_dict in data:
            self.client.execute(
                f'INSERT INTO {self._database}.{self._table} VALUES',
                event_dict,
            )

    def create_database(self):
        """
        Создаем БД, если она отсутствует
        """
        self.client.execute(f'CREATE DATABASE IF NOT EXISTS {self._database} ON CLUSTER {self._cluster}')

    def create_table(self):
        """
        Создаем таблицу, если она отсутствует
        """
        self.client.execute(f'CREATE TABLE IF NOT EXISTS {self._database}.{self._table} ON CLUSTER {self._cluster} '
                            '(id Int64, x Int32) Engine=MergeTree() ORDER BY id')

    def close(self):
        self.client.disconnect()
        self._client = None
