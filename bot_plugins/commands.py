from .filters import registered, sender_verbose, admin_verbose
from pyrogram import Client, filters
from .redis_client import set_dict
from alpha.models import Cargo
from .utils import *
from .texts import *
import os


@Client.on_message(filters.command("start") & registered)
def start(_, message):
    user, is_admin = get_user(message.from_user)
    if is_admin:
        message.reply(start_admin)
    elif user.type == "Отправитель":
        message.reply(start_sender)
    elif user.type == "Получатель":
        message.reply(start_receiver)
    elif user.type == "Отправитель и Получатель":
        message.reply(start_sender_receiver)


@Client.on_message(filters.command("admin") & registered & admin_verbose)
def admin(_, message):
    button_text = "Зайти в админ панель"
    url = "https://" + os.environ["HOST_DOMAIN"] + "/admin/"
    button = InlineKeyboardButton(button_text, url=url)
    reply_markup = InlineKeyboardMarkup([[button]])

    message.reply(admin_text, reply_markup=reply_markup)


@Client.on_message(filters.command("send") & registered & sender_verbose)
def send(_, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"user:{message.from_user.id}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    reply_markup = make_reply_markup(cargo_types)

    message.reply(send_text, reply_markup=reply_markup)


@Client.on_message(filters.command("cancel") & registered & sender_verbose)
def cancel(_, message):
    redis.delete(f"user:{message.from_user.id}")
    redis.delete(f"photo_count:{message.from_user.id}")
    for i in range(1, 5):
        redis.delete(f"photo_{i}:{message.from_user.id}")
    message.reply(cancel_text)
