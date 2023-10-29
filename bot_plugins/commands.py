from .filters import registered, sender_verbose
from pyrogram import Client, filters
from .redis_client import set_dict
from alpha.models import Cargo
from .utils import *


@Client.on_message(filters.command("start") & registered)
def start(_, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.command("postavka") & registered & sender_verbose)
def postavka(_, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"user:{message.from_user.id}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    reply_markup = make_reply_markup(cargo_types)

    text = "Начата оформление поставки\n\nВыберите тип груза:"
    message.reply(text, reply_markup=reply_markup)
