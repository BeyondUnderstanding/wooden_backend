from typing import Optional

from pydantic import BaseModel, Field


class CreateObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Created')
    id: int


class UpdateObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Updated')
    id: int


class DeletedObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Deleted')
    id: int


class GetObjectSchema(BaseModel):
    id: int
