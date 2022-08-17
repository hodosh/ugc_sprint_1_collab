import typing as t
from datetime import datetime

from pydantic import BaseModel


class MovieViewEvent(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    view_range_start: int
    view_range_end: int


class ResultMovieViewEvent(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    duration: int


class UserEvent(BaseModel):
    movie_id: str
    user_id: str
    event_time: datetime
    url: str


class Message(BaseModel):
    topic: str
    body: dict[t.Any, t.Any]
