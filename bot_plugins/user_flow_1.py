from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from alpha.models import Cargo

cargo_types = ""


@Client.on_message(filters.private & filters.command("start"))
def cmd_start(client, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.private & filters.command("postavka"))
def cmd_postavka(client, message):
    global cargo_types
    text = "Начата оформление поставки\n\nВыберите тип груза:"
    cargo = Cargo.objects.all()
    cargo_types = "("
    keyboard = []
    for c in cargo:
        button = InlineKeyboardButton(c.cargo_type, callback_data=c.cargo_type)
        keyboard.append([button])
        cargo_types += c.cargo_type + "|"
    cargo_types = cargo_types[:-1] + ")"
    print(cargo_types)
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex(cargo_types))
def transport_type(client, message):
    text = "Выберите тип транспорта:"
    transports = ["Самосвал", "Вагон"]
    keyboard = []
    for t in transports:
        button = InlineKeyboardButton(t, callback_data=t)
        keyboard.append([button])
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
