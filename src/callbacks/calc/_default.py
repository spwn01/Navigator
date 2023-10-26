from telebot import TeleBot, types
import os, json
text_config = json.load(open(os.getcwd() + "\\src\\" + "config.json", encoding = 'utf-8'))
from constants import calculator_keyboard

def start(client: TeleBot, query: types.CallbackQuery, number: str|int):
    text = query.message.text
    if text == text_config['calculator_prompt']: text = ''

    client.edit_message_text(chat_id = query.message.chat.id,
                             message_id = query.message.id,
                             text = text + str(number),
                             reply_markup = calculator_keyboard)