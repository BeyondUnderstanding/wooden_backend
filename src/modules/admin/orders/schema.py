import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.modules.admin.games.schema import GameSchemaForAdmin, GameSchemaBasic, GameSchemaForAdminWithImage


class GameToBook(BaseModel):
    game: GameSchemaForAdminWithImage
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
    is_prepayment: bool
    prepayment_done: bool

    legal_id: str
    has_manager: bool
    managers_count: int
    total_price: float
    has_bonus_game: bool


class OrderModelFull(OrderModel):
    games: List[GameToBook]
    bonus_game: Optional[GameSchemaBasic]


class OrderSendMessage(BaseModel):
    message: str


class OrderChangeBonusSchema(BaseModel):
    new_bonus: int
