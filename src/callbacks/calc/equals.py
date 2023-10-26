from telebot import TeleBot, types
from constants import config
calculator_keyboard = types.InlineKeyboardMarkup()
calculator_keyboard.row(
    types.InlineKeyboardButton(config['calculator_process'], callback_data = 'calc.process')
)

banned_symbols = ['+', '-', '/', '*']

def run(client: TeleBot, query: types.CallbackQuery):
    result = query.message.text
    for symbol in banned_symbols:
        if result.startswith(symbol):
            result = result[-1:]
        if result.endswith(symbol):
            result = result[:-1]
    if result.startswith('0'):
        result = result[-1:]
    if result.startswith('.'):
        result = '0' + result
    if result.endswith('.'):
        result = result[:-1]
    if result.endswith('*('):
        result = result[:-2]
    if result == '(' or result == ')' or result == '()':
        result = 0
    difference = result.count('(') - result.count(')')
    if difference > 0:
        result = result + ')' * difference

    try:
        result = config['calculator_success'] + str(eval(result))
        if str(result).endswith('.0'): result = result[:-2]
    except:
        result = config['error_message']
    client.edit_message_text(chat_id = query.message.chat.id,
                             message_id = query.message.id,
                             text = result,
                            reply_markup = calculator_keyboard)