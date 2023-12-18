from typing import Optional, List

from pydantic import BaseModel, Field

from src.modules.admin.games.schema import GameSchema


class GameAttributeSchema(BaseModel):
    id: int
    name: str
    value: str
    is_main: Optional[bool] = Field(default=False)


class GameAttributeWOID(BaseModel):
    name: str
    value: str
    is_main: Optional[bool] = Field(default=False)


class GameAttributeCreateSchema(GameAttributeWOID):
    game_id: int


class GameAttributeCreateBulkSchema(BaseModel):
    items: List[GameAttributeCreateSchema]


class GameAttributeWithID(GameAttributeSchema):
    id: int


class GameAttributeGetSchema(GameAttributeSchema):
    game: GameSchema


class GameAttributeOptionalSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    is_main: Optional[bool] = Field(default=None)
