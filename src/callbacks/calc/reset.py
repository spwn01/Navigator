from telebot import TeleBot, types
from constants import calculator_keyboard

def run(client: TeleBot, query: types.CallbackQuery):
    try:
        client.edit_message_text(chat_id = query.message.chat.id,
                                 message_id = query.message.id,
                                 text = '0',
                                 reply_markup = calculator_keyboard)
    except:
        client.delete_message(query.message.chat.id, query.message.id)
        client.send_message(query.message.chat.id,
                            '0',
                            reply_markup = calculator_keyboard)