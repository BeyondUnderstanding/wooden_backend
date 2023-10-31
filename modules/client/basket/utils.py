import datetime
from typing import List

from models import Basket, BasketItem
from pandas import date_range


def calculate_hours(b: Basket):
    timedelta: datetime.timedelta = b.end_date - b.start_date
    total_hours = timedelta.total_seconds() // 3600
    return total_hours


def calculate_delta(start_date, end_date):
    time_range = date_range(start_date, end_date, freq='H')
    return [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in time_range]


def calculate_order(bi: List[BasketItem], b: Basket) -> tuple[int, int, bool]:
    discounts = (100, 85, 70)
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
