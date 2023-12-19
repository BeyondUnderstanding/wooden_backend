from typing import Optional, Annotated, List
from uuid import UUID

from fastapi import Header, HTTPException
from pydantic import BaseModel, Field


class CreateObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Created')
    id: int


class CreateBulkSchema(BaseModel):
    message: Optional[str] = Field(default='Items created')
    ids: List[int]


class UpdateObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Updated')
    id: int


class UpdateBulkSchema(BaseModel):
    message: Optional[str] = Field(default='Items updated')
    ids: List[int]


class DeleteBulkSchema(BaseModel):
    message: Optional[str] = Field(default='Items deleted')
    ids: List[int]


class DeletedObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Deleted')
    id: int


class GetObjectSchema(BaseModel):
    id: int


def require_uuid(x_uuid: Annotated[str | None, Header()]) -> str:
    try:
        uuid_obj = UUID(x_uuid, version=4)
        if not str(uuid_obj) == x_uuid or x_uuid is None:
            raise HTTPException(status_code=400, detail="X-UUID header invalid")
    except ValueError:
        raise HTTPException(status_code=400, detail="X-UUID header invalid")
    return x_uuid
