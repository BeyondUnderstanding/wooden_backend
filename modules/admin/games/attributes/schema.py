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
