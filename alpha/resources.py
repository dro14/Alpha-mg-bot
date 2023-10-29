from import_export import resources, fields
from .models import Delivery


class DeliveryResource(resources.ModelResource):
    status = fields.Field(
        attribute="status",
        column_name="Статус",
    )
    sent_at = fields.Field(
        attribute="sent_at",
        column_name="Дата и время отправки",
    )
    received_at = fields.Field(
        attribute="received_at",
        column_name="Дата и время доставки",
    )
    transport_type = fields.Field(
        attribute="transport_type",
        column_name="Тип транспорта",
    )
    transport_number = fields.Field(
        attribute="transport_number",
        column_name="Номер транспорта",
    )
    cargo_type = fields.Field(
        attribute="cargo_type",
        column_name="Тип груза",
    )
    weight = fields.Field(
        attribute="weight",
        column_name="Вес (кг)",
    )
    sender_address = fields.Field(
        attribute="sender_address",
        column_name="Адрес отправки",
    )
    receiver_address = fields.Field(
        attribute="receiver_address",
        column_name="Адрес доставки",
    )
    sender = fields.Field(
        attribute="sender",
        column_name="Отправитель",
    )
    receiver = fields.Field(
        attribute="receiver",
        column_name="Получатель",
    )
    comment = fields.Field(
        attribute="comment",
        column_name="Комментарий",
    )

    class Meta:
        model = Delivery
        fields = (
            "status",
            "sent_at",
            "received_at",
            "transport_type",
            "transport_number",
            "cargo_type",
            "weight",
            "sender_address",
            "receiver_address",
            "sender",
            "receiver",
            "comment",
        )
