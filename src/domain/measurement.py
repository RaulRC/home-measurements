from pydantic import BaseModel
from datetime import datetime


class Measurement(BaseModel):
    key: str
    value: float
    place: str
    room: str
    timestamp: datetime

