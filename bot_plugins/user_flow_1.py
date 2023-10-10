from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from alpha.models import Cargo, Truck, CustomUser, Delivery, Address
from pyrogram import Client, filters
from .redis_client import *


@Client.on_message(filters.private & filters.command("start"))
def cmd_start(client, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.private & filters.command("postavka"))
def flow1step1(client, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"username:@{message.from_user.username}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    set_str("cargo_types", "|".join(cargo_types))

    keyboard = []
    for c in cargo_types:
        button = InlineKeyboardButton(c, callback_data=c)
        keyboard.append([button])

    text = "Начата оформление поставки\n\nВыберите тип груза:"
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex(get_str("cargo_types")))
def flow1step2(client, query):
    user_data = get_dict(f"username:@{query.from_user.username}")
    user_data["cargo_type"] = query.data
    user_data["current"] = "transport_type"
    set_dict(f"username:@{query.from_user.username}", user_data)

    transport_types = ["Самосвал", "Вагон"]

    keyboard = []
    for t in transport_types:
        button = InlineKeyboardButton(t, callback_data=t)
        keyboard.append([button])

    text = "Выберите тип транспорта:"
    query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("Самосвал|Вагон"))
def flow1step3(client, query):
    user_data = get_dict(f"username:@{query.from_user.username}")
    user_data["transport_type"] = query.data
    user_data["current"] = "transport_number"
    set_dict(f"username:@{query.from_user.username}", user_data)

    if query.data == "Самосвал":
        truck_numbers = Truck.objects.values_list("number", flat=True)
        set_str("trucks", "|".join(truck_numbers))

        keyboard = []
        for t in truck_numbers:
            button = InlineKeyboardButton(t, callback_data=t)
            keyboard.append([button])

        text = "Выберите государственный номер самосвала:"
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        text = "Введите номер вагона (только цифры):"
        query.edit_message_text(text)


@Client.on_callback_query(filters.regex(get_str("trucks")))
def flow1step4(client, query):
    user_data = get_dict(f"username:@{query.from_user.username}")
    user_data["transport_number"] = query.data
    user_data["current"] = "weight"
    set_dict(f"username:@{query.from_user.username}", user_data)

    text = "Введите вес груза (только цифры в кг):"
    query.edit_message_text(text)


@Client.on_message(filters.private & filters.regex(r"^\d+$"))
def flow1step5(client, message):
    user_data = get_dict(f"username:@{message.from_user.username}")
    if user_data["current"] == "transport_number":
        user_data["transport_number"] = message.text
        user_data["current"] = "weight"
        set_dict(f"username:@{message.from_user.username}", user_data)

        text = "Введите вес груза (только цифры в кг):"
        message.reply(text)

    elif user_data["current"] == "weight":
        user_data["weight"] = message.text
        user_data["current"] = "receiving_address"

        user = CustomUser.objects.get(username=message.from_user.username)
        sending_address = user.address.address
        user_data["sending_address"] = sending_address
        set_dict(f"username:@{message.from_user.username}", user_data)

        receiving_addresses = list(Address.objects.values_list("address", flat=True))
        print(receiving_addresses, type(receiving_addresses))
        receiving_addresses.remove(sending_address)
        set_str("receiving_addresses", "|".join(receiving_addresses))

        keyboard = []
        for a in receiving_addresses:
            button = InlineKeyboardButton(a, callback_data=a)
            keyboard.append([button])

        text = "Выберите адрес доставки:"
        message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex(get_str("receiving_addresses")))
def flow1step6(client, query):
    user_data = get_dict(f"username:@{query.from_user.username}")
    user_data["receiving_address"] = query.data
    user_data["current"] = "option"
    set_dict(f"username:@{query.from_user.username}", user_data)

    options = ["Утвердить", "Сбросить"]

    keyboard = []
    for o in options:
        button = InlineKeyboardButton(o, callback_data=o)
        keyboard.append([button])

    text = f"""\
Тип груза: {user_data["cargo_type"]}
Тип транспорта: {user_data["transport_type"]}
Номер транспорта: {user_data["transport_number"]}
Вес груза: {user_data["weight"]} кг
Адрес доставки: {query.data}"""
    query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("Утвердить|Сбросить"))
def flow1step7(client, query):
    user_data = get_dict(f"username:@{query.from_user.username}")
    user_data["option"] = query.data
    user_data["current"] = "end"
    set_dict(f"username:@{query.from_user.username}", user_data)

    if query.data == "Утвердить":
        text = "Поставка оформлена"
        Delivery.objects.create(
            status="Отправлен",
            transport_type=user_data["transport_type"],
            transport_number=user_data["transport_number"],
            cargo_type=user_data["cargo_type"],
            weight=user_data["weight"],
            sending_address=user_data["sending_address"],
            receiving_address=user_data["receiving_address"],
            sender=query.from_user.username,
        )
    elif query.data == "Сбросить":
        text = "Поставка отменена"
    else:
        print("unknown option:", query.data)
        return
    query.edit_message_text(text)
