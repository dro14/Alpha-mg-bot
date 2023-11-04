from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from alpha.models import User, CustomUser, Truck, Delivery
from django.utils import timezone
from .redis_client import redis
from io import BytesIO


def make_reply_markup(items):
    keyboard = []
    for item in items:
        button = InlineKeyboardButton(item, callback_data=item)
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


def user_str(user):
    return user.username if user.username else user.phone_number


def make_album(caption, user_data=None, delivery=None):
    media = []
    if user_data:
        photo_count = user_data["photo_count"]
        for i in range(1, photo_count + 1):
            media.append(
                InputMediaPhoto(
                    media=BytesIO(user_data[f"photo_{i}"]),
                    caption=caption,
                )
            )
            caption = ""
        return media
    elif delivery:
        for i in range(1, 4):
            photo = getattr(delivery, f"photo_{i}")
            if photo:
                media.append(
                    InputMediaPhoto(
                        media=BytesIO(photo),
                        caption=caption,
                    )
                )
                caption = ""
        return media


def get_user(account):
    is_admin = False
    for model in [CustomUser, User]:
        users = model.objects.all()
        for user in users:
            if user.username == account.username:
                return user, is_admin
        for user in users:
            if user.phone_number == account.phone_number:
                return user, is_admin
        is_admin = True


def get_user_id(value):
    users = CustomUser.objects.all()
    for user in users:
        if user.username == value:
            return user.user_id
    for user in users:
        if user.phone_number == value:
            return user.user_id


def update_truck(delivery, status):
    if delivery.transport_type == "Самосвал":
        truck = Truck.objects.get(number=delivery.transport_number)
        truck.status = status
        truck.save()


def get_delivery(user, user_data):
    delivery_id = int(user_data["delivery_id"])
    redis.delete(f"receiver:{user.id}")
    redis.delete(f"receiver:{user.id}:{delivery_id}")
    delivery = Delivery.objects.get(id=delivery_id)
    delivery.status = "Доставлен"
    delivery.received_at = timezone.now()
    delivery.receiver = user_str(user)
    return delivery
