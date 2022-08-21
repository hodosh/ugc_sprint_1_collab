import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME = Field(env='PROJECT_NAME', default='statistics')

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    KAFKA_TOPIC = "views"
    KAFKA_HOST = 'localhost'
    KAFKA_PORT = 9092

    KAFKA_BROKERS: list = Field(env='KAFKA_BROKERS', default=['127.0.0.1:29092', '127.0.0.1:39092'])
    KAFKA_FILM_VIEW_TOPIC: str = Field(env='KAFKA_FILM_VIEW_TOPIC', default='events_topic')


settings = Settings()
