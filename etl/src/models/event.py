from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    view_run_time: int
