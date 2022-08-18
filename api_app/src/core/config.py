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


settings = Settings()
