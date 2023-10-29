from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models


MAX_LENGTH = 255

username_validator = ASCIIUsernameValidator(
    regex=r"^[a-zA-Z0-9_]{5,32}$",
    message="Имя пользователя может содержать только заглавные (A-Z), \
    строчные (a-z) латинские буквы, цифры (0-9) и/или знак подчеркивания (_). \
    Длина имени пользователя должна быть от 5 до 32 символов.",
)

number_validator = ASCIIUsernameValidator(
    regex=r"^\d+$",
    message="Значение должно состоять только из цифр",
)


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=_("username"),
        help_text="Введите имя пользователя в Телеграме без собачки (@), например: my_username",
        validators=[username_validator],
        unique=True,
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    phone_number = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="номер телефона",
        help_text="Введите полный номер телефона Телеграм аккаунта без знака плюс (+), например: 998901234567",
        validators=[number_validator],
        blank=True,
        null=True,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким номером телефона уже существует",
        },
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        help_text="Обязательное поле. Адрес электронной почты понадобится для восстановления пароля",
    )
    user_id = models.BigIntegerField(
        verbose_name="Телеграм ID",
        null=True,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким Телеграм ID уже существует",
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username if self.username else self.phone_number

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

    objects = models.Manager()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"
        ordering = ("id",)


class CustomUser(models.Model):
    username = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=_("username"),
        help_text="Введите имя пользователя в Телеграме без собачки (@), например: my_username",
        validators=[username_validator],
        blank=True,
        null=True,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    phone_number = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="номер телефона",
        help_text="Введите полный номер телефона Телеграм аккаунта без знака плюс (+), например: 998901234567",
        validators=[number_validator],
        blank=True,
        null=True,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким номером телефона уже существует",
        },
    )
    user_id = models.BigIntegerField(
        verbose_name="Телеграм ID",
        null=True,
        unique=True,
        error_messages={
            "unique": "Пользователь с таким Телеграм ID уже существует",
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
    sender_address = models.ForeignKey(
        Address,
        verbose_name="адрес отправителя",
        on_delete=models.PROTECT,
        related_name="sending_users",
        blank=True,
        null=True,
    )
    receiver_address = models.ForeignKey(
        Address,
        verbose_name="адрес получателя",
        on_delete=models.PROTECT,
        related_name="receiving_users",
        blank=True,
        null=True,
    )

    objects = models.Manager()

    def __str__(self):
        return self.username if self.username else self.phone_number

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("id",)


class Truck(models.Model):
    number = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="самосвал",
        unique=True,
        error_messages={
            "unique": "Такой самосвал уже cуществует",
        },
    )
    datetime = models.DateTimeField(
        verbose_name="дата и время добавления",
        auto_now_add=True,
    )
    statuses = (
        ("Свободен", "Свободен"),
        ("Занят", "Занят"),
    )
    status = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="статус",
        choices=statuses,
    )

    objects = models.Manager()

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

    objects = models.Manager()

    def __str__(self):
        return self.cargo_type

    class Meta:
        verbose_name = "груз"
        verbose_name_plural = "грузы"
        ordering = ("id",)


def char_field(verbose_name, null=False):
    return models.CharField(
        max_length=MAX_LENGTH,
        verbose_name=verbose_name,
        null=null,
    )


class Delivery(models.Model):
    status = char_field("статус")
    sent_at = models.DateTimeField(
        verbose_name="дата и время отправки", default=timezone.now
    )
    received_at = models.DateTimeField(verbose_name="дата и время доставки", null=True)
    transport_type = char_field("тип транспорта")
    transport_number = char_field("номер транспорта")
    cargo_type = char_field("тип груза")
    weight = char_field("вес (кг)")
    sender_address = char_field("адрес отправки")
    receiver_address = char_field("адрес доставки")
    sender = char_field("отправитель")
    receiver = char_field("получатель", True)
    photo_1 = models.BinaryField(null=True)
    photo_2 = models.BinaryField(null=True)
    photo_3 = models.BinaryField(null=True)
    comment = models.TextField(verbose_name="комментарий", null=True)
    photo_4 = models.BinaryField(null=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.transport_type} {self.transport_number} | {self.weight} кг {self.cargo_type}"

    class Meta:
        verbose_name = "поставка"
        verbose_name_plural = "поставки"
