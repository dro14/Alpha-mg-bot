from alpha.models import Delivery
from .utils import *


def confirm_delivery(_, query, __):
    delivery = Delivery.objects.get(id=int(query.data))
    delivery.status = "Доставлен"
    delivery.received_at = timezone.now()
    delivery.receiver_verbose = user_str(query.from_user)
    delivery.save()
    query.edit_message_text("Поставка принята")
