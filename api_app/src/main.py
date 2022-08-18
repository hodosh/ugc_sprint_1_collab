import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import aiokafka

from api.v1 import events
from core.config import settings
from db import kafka

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    kafka.kafka_producer = aiokafka.AIOKafkaProducer(bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}')
    await kafka.kafka_producer.start()


@app.on_event('shutdown')
async def shutdown():
    await redis.redis.close()
    # await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix='/api/v1/event', tags=['Event'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
