from telebot import TeleBot, types
from constants import calculator_keyboard, config

special_symbols = ['+', '-', '*', '/', '^']

def run(client: TeleBot, query: types.CallbackQuery):
    text = calculate(query.message.text)

    client.edit_message_text(chat_id = query.message.chat.id,
                            message_id = query.message.id,
                            text = text,
                            reply_markup = calculator_keyboard)

def calculate(text: str) -> str:
    if text == '0' or text == config['calculator_prompt']: return '(',
    elif len(text.replace('(', '')) == 0:
        return text + '('
    else:
        for symbol in special_symbols:
            if text.endswith(symbol):
                return text + '('

        open_count = text.count('(')
        close_count = text.count(')')
        if open_count > close_count:
            if text.endswith('('):
                return text + '('
            else: return text + ')'
        elif open_count == close_count:
            return text + '*('
