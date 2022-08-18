from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from api.v1.view_models import StatusMessage
from services.event_service import EventService
from services.service_locator import get_event_service

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary="Post event message info",
    description="Post event message info"
)
async def message(topic: str, key: str, value: str,
                  event_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await event_service.send_message(topic, key, value)

    # raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    message = StatusMessage(head="ok", body="all ok")
    return message
