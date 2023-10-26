from telebot import TeleBot, types
from constants import calculator_keyboard, config

def run(client: TeleBot, query: types.CallbackQuery):
    # text = query.message.text.replace(text_config['calculator_success'], '')
    text = query.message.text
    if text == config['error_message']:
        text = config['calculator_prompt']
    else: text = text.replace(config['calculator_success'], '')
    client.edit_message_text(chat_id = query.message.chat.id,
                             message_id = query.message.id,
                             text = text,
                             reply_markup = calculator_keyboard)