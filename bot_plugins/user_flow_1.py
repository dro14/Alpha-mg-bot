from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from alpha.models import Address, CustomUser, Truck, Cargo, Delivery
from .redis_client import set_dict, get_dict
from pyrogram import Client, filters
from django.utils import timezone
from .verify import verify

photos = {}


@Client.on_message(filters.command("start") & verify)
def cmd_start(_, message):
    message.reply("Привет!\n\nДобро пожаловать в AlphaM Bot!")


@Client.on_message(filters.command("postavka") & verify)
def cmd_postavka(_, message):
    user_data = {"current": "cargo_type"}
    set_dict(f"user:{message.from_user.id}", user_data)

    cargo_types = Cargo.objects.values_list("cargo_type", flat=True)
    keyboard = []
    for c in cargo_types:
        button = InlineKeyboardButton(c, callback_data=c)
        keyboard.append([button])

    text = "Начата оформление поставки\n\nВыберите тип груза:"
    message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(verify)
def handle_callback_query(client, query):
    user_data = get_dict(f"user:{query.from_user.id}")

    match user_data["current"]:
        case "cargo_type":
            user_data["cargo_type"] = query.data
            user_data["current"] = "transport_type"
            set_dict(f"user:{query.from_user.id}", user_data)

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
            set_dict(f"user:{query.from_user.id}", user_data)

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
            set_dict(f"user:{query.from_user.id}", user_data)

            text = "Введите вес груза (только цифры в кг):"
            query.edit_message_text(text)

        case "photo_2" | "photo_3":
            user = CustomUser.objects.get(user_id=query.from_user.id)
            sender_address = user.sender_address.address
            user_data["sender_address"] = sender_address
            user_data["current"] = "receiver_address"
            set_dict(f"user:{query.from_user.id}", user_data)

            receiver_addresses = Address.objects.values_list("address", flat=True)
            keyboard = []
            for a in receiver_addresses:
                if a != sender_address:
                    button = InlineKeyboardButton(a, callback_data=a)
                    keyboard.append([button])

            text = "Выберите адрес доставки:"
            query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

        case "receiver_address":
            user_data["receiver_address"] = query.data
            user_data["current"] = "option"
            set_dict(f"user:{query.from_user.id}", user_data)

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
            set_dict(f"user:{query.from_user.id}", user_data)

            if query.data == "Утвердить":
                sender = (
                    query.from_user.username
                    if query.from_user.username
                    else query.from_user.phone_number
                )

                sender_photos = {}
                photo_count = photos[f"photo_count:{query.from_user.id}"]
                for i in range(1, photo_count + 1):
                    key = f"photo_{i}:{query.from_user.id}"
                    sender_photos[f"photo_{i}"] = photos[key].getvalue()
                    photos.pop(key)

                delivery = Delivery.objects.create(
                    status="Отправлен",
                    transport_type=user_data["transport_type"],
                    transport_number=user_data["transport_number"],
                    cargo_type=user_data["cargo_type"],
                    weight=user_data["weight"],
                    sender_address=user_data["sender_address"],
                    receiver_address=user_data["receiver_address"],
                    sender=sender,
                    **sender_photos,
                )

                r_address = Address.objects.get(address=user_data["receiver_address"])
                user_ids = r_address.receiving_users.values_list("user_id", flat=True)

                text = f"""\
Поставка отправлена

Тип транспорта - {user_data["transport_type"]}
Номер транспорта - {user_data["transport_number"]}
Дата и время отправки - Дата: {timezone.now().strftime("%d.%m.%Y")} Время: {timezone.now().strftime("%H:%M:%S")}
Тип груза - {user_data["cargo_type"]}
Тоннаж (в кг) - {user_data["weight"]} кг
Адрес отправки - {user_data["sender_address"]}
Адрес доставки - {user_data["receiver_address"]}"""

                confirm = "Подтвердить получение"
                button = InlineKeyboardButton(confirm, callback_data=str(delivery.id))
                reply_markup = InlineKeyboardMarkup([[button]])

                for user_id in user_ids:
                    set_dict(f"user:{user_id}", {"current": "confirm_delivery"})
                    client.send_message(user_id, text, reply_markup=reply_markup)

                query.edit_message_text("Информация отправлена получателям")
            else:
                query.edit_message_text("Поставка отменена")

        case "confirm_delivery":
            delivery = Delivery.objects.get(id=int(query.data))
            delivery.status = "Доставлен"
            delivery.received_at = timezone.now()
            delivery.receiver = (
                query.from_user.username
                if query.from_user.username
                else query.from_user.phone_number
            )
            delivery.save()
            query.edit_message_text("Поставка принята")


@Client.on_message(filters.regex(r"^\d+$") & verify)
def handle_numbers(_, message):
    user_data = get_dict(f"user:{message.from_user.id}")

    match user_data["current"]:
        case "transport_number":
            user_data["transport_number"] = message.text
            user_data["current"] = "weight"
            set_dict(f"user:{message.from_user.id}", user_data)

            text = "Введите вес груза (только цифры в кг):"
            message.reply(text)

        case "weight":
            user_data["weight"] = message.text
            user_data["current"] = "photo_1"
            set_dict(f"user:{message.from_user.id}", user_data)

            text = "Загрузите первое фото груза:\n\n(Чтобы загрузить, нажмите кнопку ниже в виде скрепки)"
            message.reply(text)


@Client.on_message(filters.photo & verify)
def handle_photo(client, message):
    user_data = get_dict(f"user:{message.from_user.id}")

    match user_data["current"]:
        case "photo_1" | "photo_2":
            current = user_data["current"]
            user_data[current] = message.photo.file_id
            user_data["current"] = f"photo_{int(current[-1:]) + 1}"
            set_dict(f"user:{message.from_user.id}", user_data)

            key = f"{current}:{message.from_user.id}"
            photos[key] = client.download_media(
                message.photo.file_id,
                in_memory=True,
            )

            enough = "Достаточно"
            button = InlineKeyboardButton(enough, callback_data=enough)
            reply_markup = InlineKeyboardMarkup([[button]])

            if current.endswith("1"):
                text = "Загрузите второе фото:"
                photos[f"photo_count:{message.from_user.id}"] = 1
            else:
                text = "Загрузите третье фото:"
                photos[f"photo_count:{message.from_user.id}"] = 2
            message.reply(text, reply_markup=reply_markup)

        case "photo_3":
            user = CustomUser.objects.get(user_id=message.from_user.id)
            sender_address = user.sender_address.address
            user_data["sender_address"] = sender_address
            user_data["photo_3"] = message.photo.file_id
            user_data["current"] = "receiver_address"
            set_dict(f"user:{message.from_user.id}", user_data)

            key = f"photo_3:{message.from_user.id}"
            photos[key] = client.download_media(
                message.photo.file_id,
                in_memory=True,
            )

            receiver_addresses = Address.objects.values_list("address", flat=True)
            keyboard = []
            for a in receiver_addresses:
                if a != sender_address:
                    button = InlineKeyboardButton(a, callback_data=a)
                    keyboard.append([button])

            text = "Выберите адрес доставки:"
            photos[f"photo_count:{message.from_user.id}"] = 3
            message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
