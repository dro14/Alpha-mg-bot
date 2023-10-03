from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


MAX_LENGTH = 255

username_validator = ASCIIUsernameValidator(
    regex=r"^[a-zA-Z0-9_]{5,32}$",
    message="Имя пользователя может содержать только заглавные (A-Z), \
    строчные (a-z) латинские буквы, цифры (0-9) и/или знак подчеркивания (_)",
)

number_validator = ASCIIUsernameValidator(
    regex=r"^[1-9][0-9]+$",
    message="Значение должно состоять только из цифр",
)


class User(AbstractUser):
    username = models.CharField(
        max_length=32,
        verbose_name="Telegram-username",
        help_text="Обязательное поле. Введите имя пользователя в Телеграме без собачки, например: my_username",
        validators=[username_validator],
        unique=True,
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        help_text="Обязательное поле. Введите адрес электронной почты, например: someone@example.com",
        error_messages={
            "unique": "Пользователь с таким адресом электронной почты уже существует",
        },
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "администратор"
        verbose_name_plural = "администраторы"
        ordering = ("id",)


class Address(models.Model):
    address = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="адрес",
        unique=True,
        error_messages={
            "unique": "Такой адрес уже cуществует",
        },
    )

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"
        ordering = ("id",)


class CustomUser(models.Model):
    username = models.CharField(
        max_length=32,
        verbose_name="Telegram-username",
        help_text="Обязательное поле. Введите имя пользователя в Телеграме без собачки, например: my_username",
        validators=[username_validator],
        unique=True,
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    phone_number = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="номер телефона",
        help_text="Обязательное поле. Введите номер телефона без знака плюс (+), например: 998901234567",
        validators=[number_validator],
        unique=True,
        error_messages={
            "unique": "Пользователь с таким номером телефона уже существует",
        },
    )
    types = (
        ("Отправитель", "Отправитель"),
        ("Получатель", "Получатель"),
        ("Отправитель и Получатель", "Отправитель и Получатель"),
    )
    type = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="тип пользователя",
        choices=types,
    )
    sending_address = models.ForeignKey(
        Address,
        verbose_name="адрес отправки",
        on_delete=models.PROTECT,
        related_name="sending_users",
    )
    receiving_address = models.ForeignKey(
        Address,
        verbose_name="адрес доставки",
        on_delete=models.PROTECT,
        related_name="receiving_users",
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("id",)


class Truck(models.Model):
    number = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="государственный номер",
        unique=True,
        error_messages={
            "unique": "Такой самосвал уже cуществует",
        },
    )
    datetime = models.DateTimeField(
        verbose_name="дата и время добавления",
        auto_now_add=True,
    )

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "самосвал"
        verbose_name_plural = "самосвалы"
        ordering = ("id",)


class Cargo(models.Model):
    cargo_type = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="тип груза",
        unique=True,
        error_messages={
            "unique": "Такой тип груза уже cуществует",
        },
    )

    def __str__(self):
        return self.cargo_type

    class Meta:
        verbose_name = "груз"
        verbose_name_plural = "грузы"
        ordering = ("id",)


def char_field(verbose_name):
    return models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=verbose_name,
    )


class Delivery(models.Model):
    status = char_field("статус")
    sent_at = models.DateTimeField(
        verbose_name="дата и время отправки", default=timezone.now
    )
    received_at = models.DateTimeField(
        verbose_name="дата и время доставки", blank=True, null=True
    )
    transport_type = char_field("тип транспорта")
    transport_number = char_field("номер транспорта")
    cargo_type = char_field("тип груза")
    weight = models.IntegerField(verbose_name="вес (кг)")
    sending_address = char_field("адрес отправки")
    receiving_address = char_field("адрес доставки")
    sender = char_field("отправитель")
    receiver = char_field("получатель")

    def __str__(self):
        return self.sent_at

    class Meta:
        verbose_name = "поставка"
        verbose_name_plural = "поставки"
