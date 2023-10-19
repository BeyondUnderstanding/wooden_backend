from typing import Optional

from pydantic import BaseModel, Field


class CreateImageSchema(BaseModel):
    game_id: int
    link: str
    priority: Optional[int] = Field(default=0)


class UpdateImageSchema(BaseModel):
    id: int
    game_id: Optional[int] = Field(default=None)
    link: Optional[str] = Field(default=None)
    priority: Optional[int] = Field(default=None)


class ImageSchema(BaseModel):
    id: int
    game_id: int
    link: str
    priority: int
