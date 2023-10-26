from telebot import TeleBot as __TeleBot, types as __types
import os as __os
from glob import glob as __glob
import imp as __imp
import sys as __sys
import importlib.util as __importlib

__srcpath = __os.getcwd() + "\\src\\"
__cmddir = __srcpath + "commands\\"
__calldir = __srcpath + "callbacks\\"

from constants import config as __config

def run_commands(client: __TeleBot, message: __types.Message):
    # Getting commands list.
    commands = update_commands(client)
    args = get_args(client, message)

    # Checking if the command is valid.
    user_cmd = message.text.replace('/', '', 1).replace(args, '', 1)
    if user_cmd.endswith(' ') or user_cmd.startswith(' '):
        user_cmd = ' '.join(user_cmd.split())
    for cmd in commands:
        if cmd['name'] == user_cmd:
            return __run_command(client, cmd, message)
        else:
            for ali in cmd['aliases']:
                ali = str(ali).replace('/', '')
                if len(ali) > 0 and ali == user_cmd:
                    return __run_command(client, cmd, message)

    # If there were no command.
    client.send_message(message.chat.id, __config['invalid_command'])

def update_commands(client: __TeleBot) -> list:
    # Creating global variables.
    commands = []
    telegram_cmds = []

    # Getting a commands from directories.
    for _dir in [f.path for f in __os.scandir(__cmddir) if f.is_dir()]:
        if _dir.replace(__cmddir, '') == "__pycache__":
            continue

        __sys.path.append(_dir)

        for cmd in __get_commands(_dir + '\\'):
            commands.append(cmd)
        for tg_cmd in __get_commands(_dir + '\\', 'telegram'):
            telegram_cmds.append(tg_cmd)

    client.set_my_commands(telegram_cmds)
    return commands

def get_args(client: __TeleBot, message: __types.Message) -> str:
    # Setting up variables
    data = update_commands(client)
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

def run_callbacks(client: __TeleBot, query: __types.CallbackQuery):
    # Getting callbacks list
    callbacks = update_callbacks()

    # Checking if the callback is valid.
    for call in callbacks:
        if call['name'] == __callback_filter(query.data, 'setup'):
            return __run_callback(client, call, query)

    # If there were no callback.
    client.send_message(query.message.chat.id, __config['error_message'])

def update_callbacks() -> list:
    # Creating global variables.
    callbacks = []

    # Getting a callback from directories.
    for _dir in [f.path for f in __os.scandir(__calldir) if f.is_dir()]:
        if _dir.replace(__calldir, '') == "__pycache":
            continue

        __sys.path.append(_dir)

        for callback in __get_callbacks(_dir + '\\'):
            callbacks.append(callback)

    return callbacks

# Stuff
def __run_command(cli: __TeleBot, cmd: str, msg: __types.Message):
    # Setting up a directory
    directory = f"{__cmddir}{cmd['category']}\\"

    # Getting every file from dir
    for file in __glob(directory + "*.py"):
        # Checking if the file is what we need
        name = file.replace(directory, '', 1)
        if name.replace(".py", '') != cmd['name']:
            # If the file doesn't match
            continue

        # Getting data from the file
        data = __imp.load_source(name, file)

        # Running the file
        data.run(cli, msg)

def __get_commands(cmddir: str, type: str = "commands") -> list:
    telegram_cmds = []
    commands = []

    for file in __glob(cmddir + "*.py"):
        file_name = file.replace(cmddir, '', 1)
        loader = __importlib.spec_from_file_location(file_name.replace('.py', ''), file)
        module = __importlib.module_from_spec(loader)
        loader.loader.exec_module(module)

        if type == 'commands':
            aliases = []
            if len(module.aliases['en']) > 0:
                for ali in module.aliases['en']:
                    aliases.append('/' + ali)
            if len(module.aliases['ua']) > 0:
                for ali in module.aliases['ua']:
                    aliases.append('/' + ali)

            obj = {
                "name": module.name,
                "description": module.description,
                "aliases": aliases,
                "usage": (lambda us: us if len(str(us)) > 0 else 'Немає пояснення використання\.')(module.usage),
                "category": cmddir.replace(__cmddir, '').replace('\\' + module.name, '').replace('\\', ''),
            }
            commands.append(obj)
        else:
            if file_name == 'test.py':
                continue
            telegram_cmds.append(__types.BotCommand(file_name.replace('.py', '', 1), module.description))

    if type == "commands":
        return commands
    else: return telegram_cmds

def __run_callback(cli: __TeleBot, callback, query: __types.CallbackQuery):
    # Setting up a directory
    directory = f"{__calldir}{callback['category']}\\{callback['name']}.py"

    # Getting data from the file
    data = __imp.load_source(callback['name'], directory)

    # Running the file
    data.run(cli, query)

def __get_callbacks(calldir: str) -> list:
    callbacks = []

    for file in __glob(calldir + "*.py"):
        file_name = file.replace(__calldir, '', 1).replace('.py', '')
        category = calldir.replace(__calldir, '').replace('\\', '').replace(file_name, '')
        # loader = __importlib.spec_from_file_location(file_name, file)
        # module = __importlib.module_from_spec(loader)
        # loader.loader.exec_module(module)

        obj = {
            "name": file_name.replace(category + '\\', ''),
            "category": category,
        }
        callbacks.append(obj)

    return callbacks

def __callback_filter(name: str, category: str) -> str:
    # Filter callback name
    global callback_name
    filtered = {
        'calc': name.replace('calc.', '', 1),
        'util': name.replace('util.', '', 1),
    }

    # Callback name management
    if category and category == 'category':
        if category == 'calc':
            callback_name = filtered['calc']
        elif category == 'util':
            callback_name = filtered['util']
    elif category:
        if name.startswith('calc.'):
            callback_name = filtered['calc']
        elif name.startswith('util.'):
            callback_name = filtered['util']
    else:
        return TypeError('Invalid arguments.')

    return callback_name