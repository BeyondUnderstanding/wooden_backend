from typing import Type

from sqlalchemy.orm import Session

from src.models import Book
from src.utils import sms


def send_sms_message(order_id: int, session: Session, message: str) -> bool:
    order: Type[Book] = session.get_one(Book, order_id)
    try:
        sms.SMS.send_single_message(
            message=message, to=order.client_phone, sender_id='WoodenGames'
        )
    except Exception as e:
        return False
    return True
