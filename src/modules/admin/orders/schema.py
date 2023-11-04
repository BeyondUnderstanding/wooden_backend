import datetime
from typing import List

from pydantic import BaseModel

from src.modules.admin.games.schema import GameSchemaWithID


class AGameToOrderSchema(BaseModel):
    game: GameSchemaWithID


class AOrderFullSchema(BaseModel):
    id: int
    date: datetime.datetime
    client_name: str
    client_phone: str
    is_payed: bool
    is_refunded: bool
    is_canceled: bool
    legal_id: str
    has_manager: bool
    managers_count: int
    total_price: float
    games: List[AGameToOrderSchema]
