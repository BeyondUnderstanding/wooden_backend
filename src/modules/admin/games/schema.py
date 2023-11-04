from typing import Optional, List
from pydantic import BaseModel, Field
from ..images.schemas import ImageSchema


class GameSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str
    price: float


class GameSchemaReturn(GameSchema):
    id: int
    sales_count: int
    images: List[ImageSchema]


class GameSchemaUpdate(BaseModel):
    id: int
    title: Optional[str] = Field(default='')
    description: Optional[str] = Field(default='')
    price: Optional[float] = Field(default=0)


# Беру гран-при в конкурсе на самый убогий хак против циклического импорта
def get_att_schema():
    from .attributes.schema import GameAttributeSchema
    return GameAttributeSchema


class GameSchemaWithAttributes(GameSchemaReturn):
    attributes: List[get_att_schema()]

    class Config:
        from_attributes = True


class GameSchemaWithID(GameSchema):
    id: int
