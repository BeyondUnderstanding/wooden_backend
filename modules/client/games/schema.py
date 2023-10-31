from pydantic import BaseModel


class GameSchema(BaseModel):
    id: int
    title: str
    price: float
    is_available: bool

    class Config:
        orm_mode = True


