from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from django.utils import timezone
from .redis_client import redis
from io import BytesIO


def make_reply_markup(items):
    keyboard = []
    for item in items:
        button = InlineKeyboardButton(item, callback_data=item)
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


def end_message(user_data):
    return f"""\
Тип транспорта - {user_data["transport_type"]}
Номер транспорта - {user_data["transport_number"]}
Тип груза - {user_data["cargo_type"]}
Вес груза - {user_data["weight"]} кг
Адрес отправки - {user_data["sender_address"]}
Адрес доставки - {user_data["receiver_address"]}"""


def confirm_delivery_message(user_data):
    return f"""\
Тип транспорта - {user_data["transport_type"]}
Номер транспорта - {user_data["transport_number"]}
Тип груза - {user_data["cargo_type"]}
Вес груза - {user_data["weight"]} кг
Адрес отправки - {user_data["sender_address"]}
Адрес доставки - {user_data["receiver_address"]}
Дата и время отправки - {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}"""


def user_str(user):
    return user.username if user.username else user.phone_number


def make_album(caption, photos=None, user_id=None):
    media = []
    if photos:
        for photo in photos.values():
            media.append(
                InputMediaPhoto(
                    media=BytesIO(photo),
                    caption=caption,
                )
            )
            caption = ""
        return media
    else:
        photo_count = int(redis.get(f"photo_count:{user_id}"))
        for i in range(1, photo_count + 1):
            key = f"photo_{i}:{user_id}"
            media.append(
                InputMediaPhoto(
                    media=BytesIO(redis.get(key)),
                    caption=caption,
                )
            )
            caption = ""
        return media
