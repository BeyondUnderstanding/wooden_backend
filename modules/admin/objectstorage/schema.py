from pydantic import BaseModel, Field


class UploadResponseSchema(BaseModel):

    url: str = Field(examples=['https://storage.yandexcloud.net/wooden/123.jpg'])