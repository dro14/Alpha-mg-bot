from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from alpha.models import CustomUser, Truck, Delivery
from django.utils import timezone
from .redis_client import redis
from io import BytesIO
import pytz


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
    tz = pytz.timezone("Asia/Tashkent")
    return f"""\
Груз отправлен    

Тип транспорта - {user_data["transport_type"]}
Номер транспорта - {user_data["transport_number"]}
Тип груза - {user_data["cargo_type"]}
Вес груза - {user_data["weight"]} кг
Адрес отправки - {user_data["sender_address"]}
Адрес доставки - {user_data["receiver_address"]}
Дата и время отправки - {timezone.now().astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")}"""


def complete_delivery_message(delivery):
    if not delivery.comment:
        delivery.comment = "отсутствует"
    tz = pytz.timezone("Asia/Tashkent")
    return f"""\
Груз доставлен    

Тип транспорта - {delivery.transport_type}
Номер транспорта - {delivery.transport_number}
Тип груза - {delivery.cargo_type}
Вес груза - {delivery.weight} кг
Адрес отправки - {delivery.sender_address}
Адрес доставки - {delivery.receiver_address}
Дата и время отправки - {delivery.sent_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")}
Дата и время доставки - {delivery.received_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")}
Комментарий - {delivery.comment}"""


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


def found_match(users, attr, value):
    for user in users:
        if getattr(user, attr) == value:
            return user.user_id


def get_user_id(value):
    users = CustomUser.objects.all()
    user_id = found_match(users, "username", value)
    if user_id:
        return user_id
    user_id = found_match(users, "phone_number", value)
    if user_id:
        return user_id


def update_truck(delivery, status):
    if delivery.transport_type == "Самосвал":
        truck = Truck.objects.get(number=delivery.transport_number)
        truck.status = status
        truck.save()


def get_delivery(user, user_data):
    delivery_id = int(user_data["delivery_id"])
    redis.delete(f"user:{user.id}")
    delivery = Delivery.objects.get(id=delivery_id)
    delivery.status = "Доставлен"
    delivery.received_at = timezone.now()
    delivery.receiver = user_str(user)
    return delivery
