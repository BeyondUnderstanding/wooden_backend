import telebot
from src.config import TELEBOT_TOKEN, TELEBOT_GROUP
from src.models import Book

bot = telebot.TeleBot(TELEBOT_TOKEN)


def new_order_notification(order: Book):
    bot.send_message(
        TELEBOT_GROUP, f'New order {order.id}. Date: {order.start_date}. Amount: {order.total_price}'
    )