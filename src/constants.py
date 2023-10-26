from telebot import types as __types
import os as __os, json as __json

src_path = __os.getcwd() + '\\src\\'
config = __json.load(open(src_path + 'config.json', encoding = 'utf-8'))

calculator_keyboard = __types.InlineKeyboardMarkup()
calculator_keyboard.row(   __types.InlineKeyboardButton('C', callback_data = 'calc.reset'),
                __types.InlineKeyboardButton('()', callback_data = 'calc.brackets'),
                __types.InlineKeyboardButton('<=', callback_data = 'calc.back'),
                __types.InlineKeyboardButton('/', callback_data = 'calc.divide')  )

calculator_keyboard.row(   __types.InlineKeyboardButton('7', callback_data = 'calc.7'),
                __types.InlineKeyboardButton('8', callback_data = 'calc.8'),
                __types.InlineKeyboardButton('9', callback_data = 'calc.9'),
                __types.InlineKeyboardButton('*', callback_data = 'calc.multiply')  )

calculator_keyboard.row(   __types.InlineKeyboardButton('4', callback_data = 'calc.4'),
                __types.InlineKeyboardButton('5', callback_data = 'calc.5'),
                __types.InlineKeyboardButton('6', callback_data = 'calc.6'),
                __types.InlineKeyboardButton('-', callback_data = 'calc.subtract')  )

calculator_keyboard.row(   __types.InlineKeyboardButton('1', callback_data = 'calc.1'),
                __types.InlineKeyboardButton('2', callback_data = 'calc.2'),
                __types.InlineKeyboardButton('3', callback_data = 'calc.3'),
                __types.InlineKeyboardButton('+', callback_data = 'calc.combine')  )

calculator_keyboard.row(   __types.InlineKeyboardButton('+/-', callback_data = 'calc.negative'),
                __types.InlineKeyboardButton('0', callback_data = 'calc.0'),
                __types.InlineKeyboardButton(',', callback_data = 'calc.point'),
                __types.InlineKeyboardButton('=', callback_data = 'calc.equals')  )
