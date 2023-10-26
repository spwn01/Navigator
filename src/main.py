from telebot import TeleBot, types

from dotenv import load_dotenv
load_dotenv()
import os
token = os.environ.get('TOKEN')

client = TeleBot(token)

from handler import run_commands, run_callbacks

@client.message_handler()
def on_message(message: types.Message):
        run_commands(client, message)

@client.callback_query_handler(func=lambda call: True)
def on_callback(query):
        run_callbacks(client, query)

print(f"{client.user.first_name} is running ✅")
client.polling(none_stop=False, interval=0)