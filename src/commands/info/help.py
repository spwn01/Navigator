from telebot import TeleBot, types
from handler import update_commands, get_args
from constants import config

alphabet = config['alphabet']

name = 'help'
description = 'Показує меню команд (загальний список | інформація).'
aliases = {
    'en': ['info', 'menu'],
    'ua': ['допомога'],
}
usage = '/help \(назва команди \| назва параметру\)'

translate = {
    "info": "інформація",
    "utility": "утиліти",
}
params = ['назва', alphabet['n'], 'name', 'n',
          'опис', alphabet['o'], 'o', 'description', 'd',
          'синоніми', alphabet['s'], 'c', 'synonyms', 's', 'aliases', 'a',
          'використання', alphabet['v'], 'v', 'usage', 'u']

def run(client: TeleBot, message: types.Message):
    # Setting up global variables
    args = get_args(client, message)
    data = update_commands(client)
    raw_commands = []
    categories = []

    # Getting every command from client
    for command in data:
        for parameter in params:
            if args == parameter: return parameters(args, client, message)
        # Check if user want to get an exact command
        if args and args.startswith(command['name']):
            return get_command(client, message, command)
        else:
            for ali in command['aliases']:
                ali = ali.replace('/', '')
                if args.startswith(ali):
                    return get_command(client, message, command)

        # Modifying global variables
        if command['category'] not in categories:
            categories.append(command['category'])
        if command['name'] not in raw_commands:
            raw_commands.append({
                "name": command['name'],
                "category": command['category'],
            })

    # Handling command section for the text
    commands = []
    for cat in categories:
        _sorted = []
        for cmd in raw_commands:
            # print(cmd)
            if cmd['category'] == cat:
                _sorted.append(cmd['name'])

        commands.append(f"""
*{translate[cat].capitalize()}:*
\- /{", /".join(_sorted)}
        """)

    # Creating the text
    text = f"""
\| *Список команд телеграм бота {client.user.first_name}*
📬 Потрібна допомога? Ось yci мої команди\.
{''.join(commands)}
Використовуйте /help, a потім назву команди, щоб отримати більше додаткової інформації про команду\. Наприклад: `/help інформація`\.
    """

    # Sending our result
    client.send_message(message.chat.id, text, parse_mode='markdownv2')

def get_command(client: TeleBot, message: types.Message, command):
    _description = str(command['description']).replace('.', '\.').replace('(', '\(').replace(')', '\)').replace('|', '\|')
    error_text = "Немає синонімів\."

    text = f"""
\| *Інформація стосовно команди _{command['name']}_*
📬 Якщо якийсь з пунктів був не зрозумілим, використайте */help [назва пункту]*\. Наприклад: `/help синоніми`\.

*Назва*: {command['name']} \(/{command['name']}\)
*Опис*: {_description}
*Синоніми*: {(lambda aliases: error_text if len(aliases) == 0 else ', '.join(aliases))(command['aliases'])}
*Використання*: {command['usage']}

Використовуйте /help, щоб переглянути список всіх команд {client.user.full_name}\.
    """

    client.send_message(message.chat.id, text, parse_mode='markdownv2')

# * Bold text - *text*
# * Italic text - _text_
# * Underlined text - __text__
# * Strikethrough text - ~text~
# * Spoilered text - ||text||
# * Copyable text - `text`

def parameters(args: str, client: TeleBot, message: types.Message):
    filtered = args.lower()

    if filtered == 'назва' or filtered == alphabet['n'] or 'name' or filtered == 'n':
        text = f"""
\| *Інформація стосовно пункту _Haзвa кoмaнди_*
📬 Використовуйте /help, щоб переглянути список всіх команд {client.user.full_name}\.

Цей пункт показує назву команди, завдяки якій можна з легкістью виповнити команду\. Просто напишіть: */[назва команди]*\.

Приклади: /start, `/calculator`\.

__Taкoж ви можете не писати */*, я всеодно зрозумію що ви хотіли сказати\.__

Доречі, ви ще можете визвати команди, написав її синонім\. Більше деталей: `/help синоніми`\.

Дякую за використання моїх команд\! Сподіваюся, що я зміг вам допомогти\.
        """
        return client.send_message(message.chat.id, text, parse_mode="markdownv2")
    elif filtered == 'опис' or filtered == alphabet['o'] or filtered == 'o' or filtered == 'description' or filtered == 'd':
        text = f"""
\| *Інформація стосовно пункту _Oпиc кoмaнди_*
📬 Використовуйте /help, щоб переглянути список всіх команд {client.user.full_name}\.

Цей пункт описує функціонал команди\. Завдяки цьому пункту можна дізнатися більше про команду, i що вона робить\.

Щоб подивитися опис конкретної команди, просто використайте `/help [назва команди]`\.

Дякую за використання моїх команд\! Сподіваюся, що я зміг вам допомогти\.
        """
        return client.send_message(message.chat.id, text, parse_mode="markdownv2")

    elif filtered == 'синоніми' or filtered == alphabet['s'] or filtered == 'c' or filtered == 'synonyms' or filtered == 's' or filtered == 'aliases' or filtered == 'a':
        text = f"""
\| *Інформація стосовно пункту _Bикopиcтaння кoмaнди_*
📬 Використовуйте /help, щоб переглянути список всіх команд {client.user.full_name}\.

Цей пункт показує синоніми команди, завдяки яким можна визвати команду навіть не написавши префіксу, чи навіть написавши назву команди українською мовою\. Просто напишіть: */[назва синоніму]*\.

Приклади: /info \(синонім команди /help\), `/допомога`, `/старт`\.

__Taкoж ви можете не писати */*, я всеодно зрозумію що ви хотіли сказати\.__

Щоб переглянути список синонімів конкретної команди, просто напишіть: `/help [назва команди]`\.

Дякую за використання моїх команд\! Сподіваюся, що я зміг вам допомогти\.
        """
        return client.send_message(message.chat.id, text, parse_mode="markdownv2")

    elif filtered == 'використання' or filtered == alphabet['v'] or filtered == 'v' or filtered == 'usage' or filtered == 'u':
        text = f"""
\| *Інформація стосовно пункту _Bикopиcтaння кoмaнди_*
📬 Використовуйте /help, щоб переглянути список всіх команд {client.user.full_name}\.

Цей пункт показує інструкцію використання: які аргументи для чого потрібні, i тому подібне\.

Щоб переглянути інструкцію використання конкретної команди, просто напишіть: `/help [назва команди]`\.

Приклад: /calculator \(приклад\)\. Дані, які знаходяться y дужках - аргументи, i вони не обов'язкові для використання \(до тих пір, поки команда не почне скаржитися\)\.

__Bи можете не писати аргументи, які вказані y використанні команди, якщо це не обов'язково\.__

Дякую за використання моїх команд\! Сподіваюся, що я зміг вам допомогти\.
        """
        return client.send_message(message.chat.id, text, parse_mode="markdownv2")

