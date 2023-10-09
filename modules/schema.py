from typing import Optional

from pydantic import BaseModel, Field


class CreateObjectSchema(BaseModel):
    message: Optional[str] = Field(default='Created')
    created_id: int
