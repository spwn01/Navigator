from telebot import TeleBot, types
from constants import calculator_keyboard, config
import os

secret_button = types.InlineKeyboardMarkup()
secret_button.row(
    types.InlineKeyboardButton(config['secret_message'], callback_data = 'calc.reset')
)

def run(client: TeleBot, query: types.CallbackQuery):
    text = query.message.text
    if text.lower() != config['alphabet']['v']:
        text = text[:-1]
        if len(text) == 0:
            text = config['calculator_prompt']
        try:
            client.edit_message_text(chat_id = query.message.chat.id,
                                    message_id = query.message.id,
                                    text = text,
                                    reply_markup = calculator_keyboard)
        except:
            return
    else:
        client.delete_message(query.message.chat.id, query.message.id)
        client.send_animation(query.message.chat.id,
                              open(os.getcwd() + "\\assets\\secret.gif", 'rb'),
                              reply_markup = secret_button)