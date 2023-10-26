from telebot import TeleBot, types
from _default import start

def run(client: TeleBot, query: types.CallbackQuery):
    start(client, query, '+')