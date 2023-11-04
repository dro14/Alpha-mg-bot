from .filters import registered, sender_verbose, admin_verbose, admin_receiver
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


@Client.on_message(filters.command("coming") & registered & admin_receiver)
def coming(_, message):
    coming_deliveries = Delivery.objects.filter(status="Отправлен")
    if coming_deliveries:
        user, is_admin = get_user(message.from_user)
        if is_admin:
            text = "Поставки в пути:"
        else:
            text = "Поставки в пути к вашему адресу:"
            coming_deliveries = coming_deliveries.filter(
                receiver_address=user.receiver_address
            )

        message.reply(text)
        for delivery in coming_deliveries:
            caption = coming_delivery_message(delivery)
            media = make_album(caption, delivery=delivery)
            message.reply_media_group(media)
    else:
        message.reply("Нет поставок в пути")


@Client.on_message(filters.command("send") & registered & sender_verbose)
def send(_, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"sender:{message.from_user.id}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    reply_markup = make_reply_markup(cargo_types)

    message.reply(send_text, reply_markup=reply_markup)


@Client.on_message(filters.command("cancel") & registered & sender_verbose)
def cancel(_, message):
    redis.delete(f"sender:{message.from_user.id}")
    message.reply(cancel_text)
