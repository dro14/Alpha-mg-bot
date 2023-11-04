from .redis_client import set_dict
from .utils import *
from .texts import *


def confirm_delivery(_, query, user_data):
    user_data["current"] = "complete_delivery"
    user_data["delivery_id"] = query.data
    set_dict(f"receiver:{query.from_user.id}", user_data)

    button_text = "Завершить поставку"
    button = InlineKeyboardButton(button_text, callback_data=button_text)
    reply_markup = InlineKeyboardMarkup([[button]])

    query.edit_message_text(complete_delivery_text, reply_markup=reply_markup)


def complete_delivery(client, query, user_data):
    delivery = get_delivery(query.from_user, user_data)
    delivery.save()

    users = User.objects.exclude(user_id=None)
    users = list(users.values_list("user_id", flat=True))
    users.append(get_user_id(delivery.sender))
    text = finish_delivery_message(delivery)
    for user_id in users:
        client.send_message(user_id, text)

    update_truck(delivery, "Свободен")
    query.edit_message_text("Поставка завершена")


def receive_comment(client, message, user_data, with_photo):
    delivery = get_delivery(message.from_user, user_data)
    if with_photo:
        bytes_io = client.download_media(message.photo.file_id, in_memory=True)
        delivery.photo_4 = bytes_io.getvalue()
        delivery.comment = message.caption
    else:
        delivery.comment = message.text
    delivery.save()

    users = User.objects.exclude(user_id=None)
    users = list(users.values_list("user_id", flat=True))
    users.append(get_user_id(delivery.sender))
    text = finish_delivery_message(delivery)
    for user_id in users:
        if with_photo:
            client.send_photo(user_id, bytes_io, caption=text)
        else:
            client.send_message(user_id, text)

    update_truck(delivery, "Свободен")
    message.reply("Поставка завершена")
