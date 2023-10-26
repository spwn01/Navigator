from telebot import TeleBot, types
from constants import calculator_keyboard, config

name = 'calculator'
description = 'Відкриває калькулятор.'
aliases = {
    'en': ['calc', 'calculate'],
    'ua': ['калькулятор'],
}
usage = '/calculator \(приклад\)'

def run(client: TeleBot, message: types.Message):
    client.send_message(message.chat.id, config['calculator_prompt'], reply_markup=calculator_keyboard, parse_mode = 'html')