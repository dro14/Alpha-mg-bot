from pyrogram import Client, filters
from .filters import registered


@Client.on_message(filters.command("start") & registered)
def start(_, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")
