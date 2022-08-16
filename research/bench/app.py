import uuid
from random import randrange
from datetime import datetime
import time
from time import sleep

from rich.progress import Progress
from rich.console import Console
from rich.table import Table

import config
from benchmarks import BATCH_SEQUENCE
from model import MovieViewEvent


class BenchMark:
    def __init__(self):
        self.tasks = {}
        self.users = [uuid.uuid4() for i in range(1, config.USER_COUNT)]
        self.movies = [uuid.uuid4() for i in range(1, config.MOVIE_COUNT)]
        self.user_movie = [self.movies[randrange(config.MOVIE_COUNT - 1)] for i in range(1, config.USER_COUNT)]
        self.movie_lengths = [randrange(config.MOVIE_MAX_LEN) for i in range(1, config.USER_COUNT)]
        self.progress = Progress()

    def benchmark_service_single(self, service):
        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

        for user_counter in range(1, config.USER_COUNT - 1):
            user_current_movie_id = self.user_movie[user_counter]
            for tick in range(1, self.movie_lengths[user_counter]):
                data = MovieViewEvent(
                    movie_id=str(user_current_movie_id),
                    user_id=str(self.users[user_counter]),
                    event_time=time_now,
                    view_run_time=tick
                )
                service.insert(data=data)

    def benchmark_service_batch(self, service):
        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
        data = []

        for user_counter in range(1, config.USER_COUNT - 1):
            user_current_movie_id = self.user_movie[user_counter]
            for tick in range(1, self.movie_lengths[user_counter]):
                row = MovieViewEvent(
                    movie_id=str(user_current_movie_id),
                    user_id=str(self.users[user_counter]),
                    event_time=time_now,
                    view_run_time=tick
                )
                data.append(row)

        service.insert_batch(data=data)

    def benchmark_service(self, storage, mode):
        self.tasks[storage] = self.progress.add_task(f"[cyan]{storage}", total=config.BATCHES - 1)
        service = BATCH_SEQUENCE[storage]['client']
        for i in range(1, config.BATCHES):
            if mode == "single":
                self.benchmark_service_single(service=service)
            if mode == "batch":
                self.benchmark_service_batch(service=service)

            self.progress.update(self.tasks[storage], advance=1)

    def run(self):
        statistics = []
        with Progress() as progress:
            self.progress = progress
            for item in BATCH_SEQUENCE:
                if BATCH_SEQUENCE[item]['use']:
                    mode = BATCH_SEQUENCE[item]['mode']
                    storage_name = BATCH_SEQUENCE[item]['storage']
                    t0 = time.time()

                    self.benchmark_service(item, mode)

                    t1 = time.time() - t0
                    row_stat = {'storage': storage_name, 'mode': mode, 'runtime': t1}
                    statistics.append(row_stat)
        return statistics

    def show_result(self, statistics):
        table = Table(title="OLAP Storage Research")

        table.add_column("Storage", style="magenta")
        table.add_column("Mode", justify="right", style="cyan", no_wrap=True)
        table.add_column("Run Time", justify="right", style="green")

        for row in statistics:
            table.add_row(row['storage'], row['mode'], f'{row["runtime"]:.3f}')

        console = Console()
        console.print(table)


if __name__ == '__main__':
    app = BenchMark()
    statistics = app.run()
    app.show_result(statistics)
