from typing import Optional

from pydantic import BaseModel, Field

from modules.admin.games.schema import GameSchema


class GameAttributeSchema(BaseModel):
    name: str
    value: str
    is_main: Optional[bool] = Field(default=False)
    icon: Optional[str] = Field(default=None)


class GameAttributeCreateSchema(GameAttributeSchema):
    game_id: int


class GameAttributeWithID(GameAttributeSchema):
    id: int


class GameAttributeGetSchema(GameAttributeSchema):
    game: GameSchema


class GameAttributeOptionalSchema(BaseModel):
    name: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    is_main: Optional[bool] = Field(default=None)
    icon: Optional[str] = Field(default=None)
