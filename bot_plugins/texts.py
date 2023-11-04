from django.utils import timezone
import pytz


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


complete_delivery_text = """Отправьте фото (1 шт) и/или комментарий. Загружать можно:

- только фото (чтобы загрузить, нажмите кнопку ниже 👇 в виде скрепки 📎)

- только комментарий (отправьте текстовое сообщение)

- фото с комментарием (при добавлении фото, поле для текста появится ниже)

Если желаете оставить пустым, нажмите кнопку \"Завершить поставку\""""


def finish_delivery_message(delivery):
    comment = ""
    if delivery.comment:
        comment = f"\nКомментарий - {delivery.comment}"
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
Дата и время доставки - {delivery.received_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")}{comment}"""


start_admin = """Добро пожаловать в AlphaM Bot!

Вы зарегистрированы в системе как администратор и у вас есть доступ к админ панели. \
Через команду ниже вы можете зайти в админ панель.

👉 /admin 👈"""

start_sender = """Добро пожаловать в AlphaM Bot!

Вы зарегистрированы в системе как отправитель и вы можете отправлять поставки. \
Через команду ниже вы можете начать оформление поставки.

👉 /send 👈"""

start_receiver = """Добро пожаловать в AlphaM Bot!

Вы зарегистрированы в системе как получатель и вам приходят уведомления о \
входящих поставках соответственно по вашему адресу."""

start_sender_receiver = """Добро пожаловать в AlphaM Bot!

Вы зарегистрированы в системе как отправитель и получатель. \
Вы можете и отправлять поставки, и получать уведомления о входящих поставках соответственно по вашему адресу. \
Через команду ниже вы можете начать оформление поставки.

👉 /send 👈"""


def coming_delivery_message(delivery):
    tz = pytz.timezone("Asia/Tashkent")
    return f"""\
Статус - {delivery.status}
Дата и время отправки - {delivery.sent_at.astimezone(tz).strftime("%d.%m.%Y %H:%M:%S")}
Тип транспорта - {delivery.transport_type}
Номер транспорта - {delivery.transport_number}
Тип груза - {delivery.cargo_type}
Вес груза - {delivery.weight} кг
Адрес отправки - {delivery.sender_address}
Адрес доставки - {delivery.receiver_address}
Отправитель - {delivery.sender}"""


admin_text = "В админ панели вы можете просмотреть и управлять данными"

send_text = "Начата оформление поставки\n\nВыберите тип груза:"

cancel_text = "Оформление поставки отменено"
