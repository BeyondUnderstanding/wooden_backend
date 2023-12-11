import datetime
from typing import List

from src.models import Basket, BasketItem, Book
from pandas import date_range
from src.utils import sms


def calculate_hours(b: Basket):
    timedelta: datetime.timedelta = b.end_date - b.start_date
    total_hours = timedelta.total_seconds() // 3600
    return total_hours


def calculate_delta(start_date, end_date):
    if not start_date or not end_date:
        return []
    time_range = date_range(start_date, end_date, freq='H')
    return [datetime.datetime.strptime(str(x).replace('+00:00', ''), '%Y-%m-%d %H:%M:%S') for x in time_range]


def calculate_order(bi: List[BasketItem], b: Basket) -> tuple[int, int, bool]:
    discounts = (1, 0.85, 0.7)
    # 0%  (100% - 0%)
    # 15% (100% - 15%)
    # 30% (100% - 30%)

    current_discount = discounts[0]
    managers_count = 0
    bonus_game = False
    games_count = len(bi)
    hours_count = calculate_hours(b)

    if (5 <= games_count < 9) and (hours_count >= 3) or \
            (3 <= games_count < 9) and (hours_count >= 5):
        current_discount = discounts[1]  # 15 %
        managers_count = 1
    elif (games_count >= 9) and (hours_count >= 5):
        current_discount = discounts[2]  # 30%
        managers_count = 2
        bonus_game = True

    return current_discount, managers_count, bonus_game


def new_order_sms_notification(book: Book):
    message = None

    if book.payment_method == 'prepayment':
        message = ''
    elif book.payment_method == 'card':
        message = ''

    return sms.SMS.send_single_message(
        message=message, to=book.client_phone, sender_id='WoodenGames'
    )