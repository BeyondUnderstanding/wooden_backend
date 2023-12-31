from typing import List

from datetime import datetime
from pydantic import BaseModel

class GameAttributeSchema(BaseModel):
    name: str
    value: str
    is_main: bool

class GameImage(BaseModel):
    link: str
    priority: int


class GameSchema(BaseModel):
    id: int
    title: str
    price: float
    is_available: bool
    images: List['GameImage']

    class Config:
        orm_mode = True

class GameSchemaFull(GameSchema):
    attributes: List['GameAttributeSchema']
    description: str


class OccupiedDateTimeSchema(BaseModel):
    datetime: datetime