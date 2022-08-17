import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME = Field(env='PROJECT_NAME', default='statistics')

    # Настройки Redis
    REDIS_HOST = Field(env='REDIS_HOST', default='127.0.0.1')
    REDIS_PORT = Field(env='REDIS_PORT', default=6379)

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    KAFKA_TOPIC = "views"
    KAFKA_HOST = 'localhost'
    KAFKA_PORT = 9092


settings = Settings()
