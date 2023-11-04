from typing import List

from pydantic import BaseModel

class GameAttributeSchema(BaseModel):
    name: str
    value: str
    is_main: bool
    icon: str

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
