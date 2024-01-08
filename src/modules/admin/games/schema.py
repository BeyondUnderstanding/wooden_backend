from typing import Optional, List
from pydantic import BaseModel, Field
from ..images.schemas import ImageSchema


class GameSchemaBasic(BaseModel):
    id: int
    title: str
    price: float
    is_deleted: bool
    images: List[ImageSchema]
    is_bonus_game: Optional[bool] = Field(default=False)

class GameSchema(BaseModel):
    title: str = Field(max_length=50)
    description: str
    price: float


class GameSchemaForAdmin(BaseModel):
    id: int
    title: str
    images: List[ImageSchema]


class GameSchemaForAdminWithImage(GameSchemaForAdmin):
    images: List[ImageSchema]


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
