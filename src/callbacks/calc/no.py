from telebot import TeleBot, types
from constants import calculator_keyboard, config

def run(client: TeleBot, query: types.CallbackQuery):
    text = query.message.text
    if text == config['calculator_prompt']:
        text = 0
        client.edit_message_text(chat_id = query.message.chat.id,
                                message_id = query.message.id,
                                text = text,
                                reply_markup = calculator_keyboard)
    else: return