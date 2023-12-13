import enum
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_serializer
from pydantic.types import AwareDatetime

from src.modules.client.games.schema import GameSchema


class AddToBasketSchema(BaseModel):
    id: int


class BasketItemWithShortInfo(BaseModel):
    game: GameSchema

class PaymentMethod(enum.Enum):
    prepayment = 'prepayment'
    card = 'card'


class CreateBooking(BaseModel):
    client_name: str
    client_phone: str = Field(pattern='^\+995[57]\d{8}$')
    client_email: EmailStr
    delivery_address: str
    extra: Optional[str] = Field(default=None)
    legal_id: str = Field(min_length=11, max_length=11, pattern="^\\d+$", )
    payment_method: PaymentMethod


class UpdateBasketDates(BaseModel):
    start_date: AwareDatetime
    end_date: AwareDatetime


class MinRequirementsException(BaseModel):
    detail: str = Field(examples=['Minimum requirements for the order are not met'],
                        description='Raises when calculate_hours(basket_obj) < 3',
                        title='MinRequirementsException')


class DatesException(BaseModel):
    detail: str = Field(examples=['Dates are invalid'],
                        description='Raises when fastapi cannot parse start_date or end_date in Basket object',
                        title='DatesException')


class EmptyBasketException(BaseModel):
    detail: str = Field(examples=['Basket empty'],
                        description='Raises when len(basket_items) == 0',
                        title='EmptyBasketException')


class CreateOrderOK(BaseModel):
    order_id: int
    payment_method: PaymentMethod
    checkout_url: Optional[str | None]

