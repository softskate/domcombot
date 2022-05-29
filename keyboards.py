from telebot.types import *
from utils import *


def get_chats():
    keys = InlineKeyboardMarkup()
    apts = Apartment.select()
    for apt in apts:
        apt: Apartment
        key = InlineKeyboardButton(f'Дом {apt.apt_id}', callback_data=f'selected_{apt.id}')
        keys.add(key)
    return keys

def get_chat(apt: Apartment):
    keys = InlineKeyboardMarkup()
    key = InlineKeyboardButton(f'Ждём вас в дом {apt.apt_id}', apt.chat_url)
    keys.add(key)
    return keys
