from typing import Optional, List

from pydantic import BaseModel, Field


class GameSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str
    price: float


class GameSchemaReturn(GameSchema):
    id: int
