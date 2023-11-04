from pyrogram.errors.exceptions.bad_request_400 import UserBlocked
from .redis_client import set_dict
from alpha.models import Address
from .utils import *
from .texts import *


def cargo_type(_, query, user_data):
    user_data["cargo_type"] = query.data
    user_data["current"] = "transport_type"
    set_dict(f"sender:{query.from_user.id}", user_data)

    transport_types = ["Самосвал", "Вагон"]
    reply_markup = make_reply_markup(transport_types)

    text = "Выберите тип транспорта:"
    query.edit_message_text(text, reply_markup=reply_markup)


def transport_type(_, query, user_data):
    user_data["transport_type"] = query.data
    user_data["current"] = "transport_number"
    set_dict(f"sender:{query.from_user.id}", user_data)

    if query.data == "Самосвал":
        truck_numbers = Truck.objects.filter(status="Свободен")
        truck_numbers = truck_numbers.values_list("number", flat=True)
        reply_markup = make_reply_markup(truck_numbers)

        text = "Выберите государственный номер самосвала:"
        query.edit_message_text(text, reply_markup=reply_markup)
    else:
        text = "Введите номер вагона (только цифры):"
        query.edit_message_text(text)


def transport_number1(_, query, user_data):
    user_data["transport_number"] = query.data
    user_data["current"] = "weight"
    set_dict(f"sender:{query.from_user.id}", user_data)

    text = "Введите вес груза (только цифры в кг):"
    query.edit_message_text(text)


def transport_number2(_, message, user_data):
    user_data["transport_number"] = message.text
    user_data["current"] = "weight"
    set_dict(f"sender:{message.from_user.id}", user_data)

    text = "Введите вес груза (только цифры в кг):"
    message.reply(text)


def weight(_, message, user_data):
    user_data["weight"] = message.text
    user_data["current"] = "photo_1"
    set_dict(f"sender:{message.from_user.id}", user_data)

    text = "Загрузите первое фото (1 шт):\n\n(Чтобы загрузить, нажмите кнопку ниже 👇 в виде скрепки 📎)"
    message.reply(text)


def photo_1_2(client, message, user_data):
    current = user_data["current"]
    user_data["current"] = f"photo_{int(current[-1:]) + 1}"

    user_data[current] = client.download_media(
        message.photo.file_id,
        in_memory=True,
    ).getvalue()

    if current.endswith("1"):
        text = "Загрузите второе фото (1 шт):"
        user_data["photo_count"] = 1
    else:
        text = "Загрузите третье фото (1 шт):"
        user_data["photo_count"] = 2
    set_dict(f"sender:{message.from_user.id}", user_data)

    enough = "Достаточно"
    button = InlineKeyboardButton(enough, callback_data=enough)
    reply_markup = InlineKeyboardMarkup([[button]])

    message.reply(text, reply_markup=reply_markup)


def photo_2_3(_, query, user_data):
    user = CustomUser.objects.get(user_id=query.from_user.id)
    sender_address = user.sender_address.address
    user_data["sender_address"] = sender_address
    user_data["sender"] = user_str(query.from_user)
    user_data["current"] = "receiver_address"
    set_dict(f"sender:{query.from_user.id}", user_data)

    receiver_addresses = Address.objects.exclude(address=sender_address)
    receiver_addresses = receiver_addresses.values_list("address", flat=True)
    reply_markup = make_reply_markup(receiver_addresses)

    text = "Выберите адрес доставки:"
    query.edit_message_text(text, reply_markup=reply_markup)


def photo_3(client, message, user_data):
    user = CustomUser.objects.get(user_id=message.from_user.id)
    sender_address = user.sender_address.address
    user_data["sender_address"] = sender_address
    user_data["sender"] = user_str(message.from_user)
    user_data["current"] = "receiver_address"

    user_data["photo_3"] = client.download_media(
        message.photo.file_id,
        in_memory=True,
    ).getvalue()
    user_data["photo_count"] = 3
    set_dict(f"sender:{message.from_user.id}", user_data)

    receiver_addresses = Address.objects.exclude(address=sender_address)
    receiver_addresses = receiver_addresses.values_list("address", flat=True)
    reply_markup = make_reply_markup(receiver_addresses)

    text = "Выберите адрес доставки:"
    message.reply(text, reply_markup=reply_markup)


def receiver_address(_, query, user_data):
    user_data["receiver_address"] = query.data
    user_data["current"] = "end"
    set_dict(f"sender:{query.from_user.id}", user_data)

    options = ["Утвердить", "Сбросить"]
    reply_markup = make_reply_markup(options)

    caption = end_message(user_data)
    media = make_album(caption, user_data=user_data)

    query.message.reply_media_group(media)
    query.message.reply("Подтверждаете введённые данные?", reply_markup=reply_markup)
    query.message.delete()


def end(client, query, user_data):
    if query.data == "Утвердить":
        caption = confirm_delivery_message(user_data)
        media = make_album(caption, user_data=user_data)

        user_data.pop("current")
        user_data.pop("photo_count")
        user_data["status"] = "Отправлен"
        delivery = Delivery.objects.create(**user_data)

        text = "При получении груза, нажмите кнопку ниже"

        button_text = "Подтвердить получение"
        button = InlineKeyboardButton(button_text, callback_data=str(delivery.id))
        reply_markup = InlineKeyboardMarkup([[button]])

        address = Address.objects.get(address=user_data["receiver_address"])
        receivers = address.receiving_users.exclude(user_id=None)
        receivers = receivers.values_list("user_id", flat=True)
        for user_id in receivers:
            set_dict(
                f"receiver:{user_id}:{delivery.id}",
                {"current": "confirm_delivery"},
            )
            try:
                client.send_media_group(user_id, media)
                client.send_message(user_id, text, reply_markup=reply_markup)
            except UserBlocked:
                pass

        admins = User.objects.exclude(user_id=None)
        admins = admins.values_list("user_id", flat=True)
        for user_id in admins:
            try:
                client.send_media_group(user_id, media)
            except UserBlocked:
                pass

        update_truck(delivery, "Занят")
        query.edit_message_text("Поставка оформлена")
    else:
        query.edit_message_text("Поставка отменена")

    redis.delete(f"sender:{query.from_user.id}")
