from pydantic import BaseModel
from datetime import datetime


class Measurement(BaseModel):
    temperature: float
    humidity: float
    place: str
    room: str
    timestamp: datetime

