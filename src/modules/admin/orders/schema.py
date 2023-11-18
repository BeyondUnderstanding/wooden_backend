import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.modules.admin.games.schema import GameSchemaForAdmin


class GameToBook(BaseModel):
    game: GameSchemaForAdmin
    game_price_before: float
    game_price_after: float


class OrderModel(BaseModel):
    id: int
    start_date: datetime.datetime
    end_date: datetime.datetime
    client_name: str
    client_phone: str
    client_email: str
    is_payed: bool
    is_refunded: bool
    is_canceled: bool
    legal_id: str
    has_manager: bool
    managers_count: int
    total_price: float
    has_bonus_game: bool


class OrderModelFull(OrderModel):
    games: List[GameToBook]
    bonus_game: Optional[GameSchemaForAdmin]
