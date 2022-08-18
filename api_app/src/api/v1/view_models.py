from typing import Optional

from models.models import ORJSONModel


class StatusMessage(ORJSONModel):
    head: str
    body: str

