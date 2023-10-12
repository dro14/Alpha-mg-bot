from alpha.models import User, Address, CustomUser, Truck, Cargo, Delivery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .redis_client import set_dict, get_dict
from pyrogram import Client, filters


@Client.on_message(filters.private)
def verify(client, message):
    for model in [CustomUser, User]:
        users = model.objects.all()
        for user in users:
            if user.username == message.from_user.username:
                if not user.user_id:
                    user.user_id = message.from_user.id
                    if message.from_user.phone_number:
                        user.phone_number = message.from_user.phone_number
                    user.save()
                return True
            if user.phone_number == message.from_user.phone_number:
                if not user.user_id:
                    user.user_id = message.from_user.id
                    if message.from_user.username:
                        user.username = message.from_user.username
                    user.save()
                return True

    message.reply("Вы не зарегистрированы в системе")
    return False


@Client.on_message(filters.private & filters.command("start"))
def cmd_start(client, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.private & filters.command("postavka"))
def cmd_postavka(client, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"user:@{message.from_user.username}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    keyboard = []
    for c in cargo_types:
        button = InlineKeyboardButton(c, callback_data=c)
        keyboard.append([button])

    text = "Начата оформление поставки\n\nВыберите тип груза:"
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query()
def handle_callback_query(client, query):
    user_data = get_dict(f"user:@{query.from_user.username}")

    match user_data["current"]:
        case "cargo_type":
            user_data["cargo_type"] = query.data
            user_data["current"] = "transport_type"
            set_dict(f"user:@{query.from_user.username}", user_data)

            transport_types = ["Самосвал", "Вагон"]
            keyboard = []
            for t in transport_types:
                button = InlineKeyboardButton(t, callback_data=t)
                keyboard.append([button])

            text = "Выберите тип транспорта:"
            query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

        case "transport_type":
            user_data["transport_type"] = query.data
            user_data["current"] = "transport_number"
            set_dict(f"user:@{query.from_user.username}", user_data)

            if query.data == "Самосвал":
                truck_numbers = Truck.objects.values_list("number", flat=True)
                keyboard = []
                for t in truck_numbers:
                    button = InlineKeyboardButton(t, callback_data=t)
                    keyboard.append([button])

                text = "Выберите государственный номер самосвала:"
                query.edit_message_text(
                    text, reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                text = "Введите номер вагона (только цифры):"
                query.edit_message_text(text)

        case "transport_number":
            user_data["transport_number"] = query.data
            user_data["current"] = "weight"
            set_dict(f"user:@{query.from_user.username}", user_data)

            text = "Введите вес груза (только цифры в кг):"
            query.edit_message_text(text)

        case "receiver_address":
            user_data["receiver_address"] = query.data
            user_data["current"] = "option"
            set_dict(f"user:@{query.from_user.username}", user_data)

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

        case "option":
            user_data["option"] = query.data
            user_data["current"] = "end"
            set_dict(f"user:@{query.from_user.username}", user_data)

            if query.data == "Утвердить":
                Delivery.objects.create(
                    status="Отправлен",
                    transport_type=user_data["transport_type"],
                    transport_number=user_data["transport_number"],
                    cargo_type=user_data["cargo_type"],
                    weight=user_data["weight"],
                    sender_address=user_data["sender_address"],
                    receiver_address=user_data["receiver_address"],
                    sender=query.from_user.username,
                )
                query.edit_message_text("Информация отправлена получателям")
            else:
                query.edit_message_text("Поставка отменена")


@Client.on_message(filters.private & filters.regex(r"^\d+$"))
def handle_numbers(client, message):
    user_data = get_dict(f"user:@{message.from_user.username}")

    match user_data["current"]:
        case "transport_number":
            user_data["transport_number"] = message.text
            user_data["current"] = "weight"
            set_dict(f"user:@{message.from_user.username}", user_data)

            text = "Введите вес груза (только цифры в кг):"
            message.reply(text)

        case "weight":
            user = CustomUser.objects.get(username=message.from_user.username)
            sender_address = user.sender_address.address
            user_data["sender_address"] = sender_address
            user_data["weight"] = message.text
            user_data["current"] = "receiver_address"
            set_dict(f"user:@{message.from_user.username}", user_data)

            receiver_addresses = Address.objects.values_list("address", flat=True)
            keyboard = []
            for a in receiver_addresses:
                if a != sender_address:
                    button = InlineKeyboardButton(a, callback_data=a)
                    keyboard.append([button])

            text = "Выберите адрес доставки:"
            message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
