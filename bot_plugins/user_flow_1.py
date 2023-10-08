from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from alpha.models import Cargo, Truck
from .redis_client import *


@Client.on_message(filters.private & filters.command("start"))
def cmd_start(client, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.private & filters.command("postavka"))
def flow1step1(client, message):
    text = "Начата оформление поставки\n\nВыберите тип груза:"
    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    keyboard = []
    for c in cargo_types:
        button = InlineKeyboardButton(c, callback_data=c)
        keyboard.append([button])
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
    set_str("cargo", "|".join(cargo_types))


@Client.on_callback_query(filters.regex(get_str("cargo")))
def flow1step2(client, query):
    text = "Выберите тип транспорта:"
    transport_types = ["Самосвал", "Вагон"]
    keyboard = []
    for t in transport_types:
        button = InlineKeyboardButton(t, callback_data=t)
        keyboard.append([button])
    query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    user_data = {"cargo": query.data, "transport_type": "?"}
    set_dict(f"user:{query.from_user.id}", user_data)


@Client.on_callback_query(filters.regex("Самосвал|Вагон"))
def flow1step3(client, query):
    user_data = get_dict(f"user:{query.from_user.id}")
    if user_data["transport_type"] != "?":
        print("transport_type already set")
        return

    if query.data == "Самосвал":
        text = "Выберите государственный номер самосвала:"
        truck_numbers = Truck.objects.values_list("number", flat=True)
        keyboard = []
        for t in truck_numbers:
            button = InlineKeyboardButton(t, callback_data=t)
            keyboard.append([button])
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        set_str("trucks", "|".join(truck_numbers))
    elif query.data == "Вагон":
        text = "Введите номер вагона (только цифры):"
        query.edit_message_text(text)
    else:
        print("unknown transport_type:", query.data)
        return

    user_data["transport_type"] = query.data
    user_data["transport_number"] = "?"
    set_dict(f"user:{query.from_user.id}", user_data)


@Client.on_callback_query(filters.regex(get_str("trucks")))
def flow1step4(client, query):
    user_data = get_dict(f"user:{query.from_user.id}")
    if user_data["transport_number"] != "?":
        print("transport_number already set")
        return

    text = "Введите вес груза (только цифры в кг):"
    query.edit_message_text(text)

    user_data["transport_number"] = query.data
    user_data["weight"] = "?"
    set_dict(f"user:{query.from_user.id}", user_data)


@Client.on_message(filters.private & filters.regex(r"^\d+$"))
def flow1step5(client, message):
    user_data = get_dict(f"user:{message.from_user.id}")
    if user_data["transport_number"] == "?":
        text = "Введите вес груза (только цифры в кг):"
        message.reply(text)
        user_data["transport_number"] = message.text
        user_data["weight"] = "?"
        set_dict(f"user:{message.from_user.id}", user_data)
    elif user_data["weight"] == "?":
        text = "Выберите адрес доставки:"
        message.reply(text)
        user_data["weight"] = message.text
        user_data["address"] = "?"
        set_dict(f"user:{message.from_user.id}", user_data)
    else:
        print("unknown message:", message.text)
