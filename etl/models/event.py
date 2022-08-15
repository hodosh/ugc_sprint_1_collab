from pydantic import BaseModel


class Event(BaseModel):
    movie_id: str
    user_id: str
    timestamp: int
