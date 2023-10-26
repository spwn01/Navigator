from telebot import TeleBot, types
import os
from constants import config

alphabet = config['alphabet']

name = 'test'
description = 'Test command'
aliases = {
    'en': [],
    'ua': [],
}
usage = ''
def run(client: TeleBot, message: types.Message):
    # client.send_animation(message.chat.id, open(os.getcwd() + "\\assets\\secret.gif", 'rb'))
    client.send_message(message.chat.id, f"{config['secret_message']} {str(alphabet['p']).capitalize()}{alphabet['r']}{alphabet['u']}{alphabet['v']}{alphabet['i']}{alphabet['t']}{alphabet['apostrophe']}")