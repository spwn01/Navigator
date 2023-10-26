# Imports
from telebot import TeleBot as __TeleBot, types as __types
from handler import update_commands as __update_commands

def get_args(client: __TeleBot, message: __types.Message) -> str:
    # Setting up variables
    data = __update_commands(client)
    filtered = message.text.replace('/', '', 1)

    # Getting every command in client
    for cmd in data:
        # Removing command name/aliase from message content
        if filtered.startswith(cmd['name']):
            filtered = filtered.replace(cmd['name'], '', 1)
        else:
            for ali in cmd['aliases']:
                ali = str(ali).replace('/', '')
                if filtered.startswith(ali):
                    filtered = filtered.replace(ali, '', 1)
    # Escaping weird content
    if filtered.startswith(' '):
        filtered = ' '.join(filtered.split())
    return filtered

