from telebot import TeleBot, types
from constants import config

name = 'start'
description = 'Розпочинає роботу клієнта.'
aliases = {
    'en': ['hello', 'hi'],
    'ua': ['старт'],
}
usage = '/start'

def run(client: TeleBot, message: types.Message):
    client.send_message(message.chat.id, config['welcome_message'].replace('{name}', message.chat.first_name))