from alpha.models import Delivery
from pyrogram import Client
from .filters import registered, receiver
from .redis_client import get_dict
from django.utils import timezone


@Client.on_callback_query(registered & receiver)
def handle_receiver_callback_query(_, query):
    user_data = get_dict(f"user:{query.from_user.id}")

    match user_data["current"]:
        case "confirm_delivery":
            delivery = Delivery.objects.get(id=int(query.data))
            delivery.status = "Доставлен"
            delivery.received_at = timezone.now()
            delivery.receiver_verbose = (
                query.from_user.username
                if query.from_user.username
                else query.from_user.phone_number
            )
            delivery.save()
            query.edit_message_text("Поставка принята")
