# Generated by Django 4.2.7 on 2023-11-08 08:00

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        error_messages={"unique": "Такой адрес уже cуществует"},
                        max_length=255,
                        unique=True,
                        verbose_name="адрес",
                    ),
                ),
            ],
            options={
                "verbose_name": "адрес",
                "verbose_name_plural": "адреса",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Cargo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cargo_type",
                    models.CharField(
                        error_messages={"unique": "Такой тип груза уже cуществует"},
                        max_length=255,
                        unique=True,
                        verbose_name="тип груза",
                    ),
                ),
            ],
            options={
                "verbose_name": "груз",
                "verbose_name_plural": "грузы",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="Delivery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=255, verbose_name="статус")),
                (
                    "sent_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="дата и время отправки",
                    ),
                ),
                (
                    "received_at",
                    models.DateTimeField(
                        null=True, verbose_name="дата и время доставки"
                    ),
                ),
                (
                    "transport_type",
                    models.CharField(max_length=255, verbose_name="тип транспорта"),
                ),
                (
                    "transport_number",
                    models.CharField(max_length=255, verbose_name="номер транспорта"),
                ),
                (
                    "cargo_type",
                    models.CharField(max_length=255, verbose_name="тип груза"),
                ),
                ("weight", models.CharField(max_length=255, verbose_name="вес (кг)")),
                (
                    "sender_address",
                    models.CharField(max_length=255, verbose_name="адрес отправки"),
                ),
                (
                    "receiver_address",
                    models.CharField(max_length=255, verbose_name="адрес доставки"),
                ),
                (
                    "sender",
                    models.CharField(max_length=255, verbose_name="отправитель"),
                ),
                (
                    "receiver",
                    models.CharField(
                        max_length=255, null=True, verbose_name="получатель"
                    ),
                ),
                ("photo_1", models.BinaryField(null=True)),
                ("photo_2", models.BinaryField(null=True)),
                ("photo_3", models.BinaryField(null=True)),
                ("comment", models.TextField(null=True, verbose_name="комментарий")),
                ("photo_4", models.BinaryField(null=True)),
            ],
            options={
                "verbose_name": "поставка",
                "verbose_name_plural": "поставки",
            },
        ),
        migrations.CreateModel(
            name="Truck",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.CharField(
                        error_messages={"unique": "Такой самосвал уже cуществует"},
                        max_length=255,
                        unique=True,
                        verbose_name="самосвал",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата и время добавления"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Свободен", "Свободен"), ("Занят", "Занят")],
                        max_length=255,
                        verbose_name="статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "самосвал",
                "verbose_name_plural": "самосвалы",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Пользователь с таким именем уже существует"
                        },
                        help_text="Введите имя пользователя в Телеграме без собачки (@), например: my_username",
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator(
                                message="Имя пользователя может содержать только заглавные (A-Z),     строчные (a-z) латинские буквы, цифры (0-9) и/или знак подчеркивания (_).     Длина имени пользователя должна быть от 5 до 32 символов.",
                                regex="^[a-zA-Z0-9_]{5,32}$",
                            )
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Пользователь с таким номером телефона уже существует"
                        },
                        help_text="Введите полный номер телефона Телеграм аккаунта без знака плюс (+), например: 998901234567",
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator(
                                message="Значение должно состоять только из цифр",
                                regex="^\\d+$",
                            )
                        ],
                        verbose_name="номер телефона",
                    ),
                ),
                (
                    "user_id",
                    models.BigIntegerField(
                        error_messages={
                            "unique": "Пользователь с таким Телеграм ID уже существует"
                        },
                        null=True,
                        unique=True,
                        verbose_name="Телеграм ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Отправитель", "Отправитель"),
                            ("Получатель", "Получатель"),
                            ("Отправитель и Получатель", "Отправитель и Получатель"),
                        ],
                        max_length=255,
                        verbose_name="тип пользователя",
                    ),
                ),
                (
                    "receiver_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="receiving_users",
                        to="alpha.address",
                        verbose_name="адрес получателя",
                    ),
                ),
                (
                    "sender_address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sending_users",
                        to="alpha.address",
                        verbose_name="адрес отправителя",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
                "ordering": ("id",),
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "Пользователь с таким именем уже существует"
                        },
                        help_text="Введите имя пользователя в Телеграме без собачки (@), например: my_username",
                        max_length=255,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator(
                                message="Имя пользователя может содержать только заглавные (A-Z),     строчные (a-z) латинские буквы, цифры (0-9) и/или знак подчеркивания (_).     Длина имени пользователя должна быть от 5 до 32 символов.",
                                regex="^[a-zA-Z0-9_]{5,32}$",
                            )
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        error_messages={
                            "unique": "Пользователь с таким номером телефона уже существует"
                        },
                        help_text="Введите полный номер телефона Телеграм аккаунта без знака плюс (+), например: 998901234567",
                        max_length=255,
                        null=True,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator(
                                message="Значение должно состоять только из цифр",
                                regex="^\\d+$",
                            )
                        ],
                        verbose_name="номер телефона",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Обязательное поле. Адрес электронной почты понадобится для восстановления пароля",
                        max_length=254,
                        verbose_name="email address",
                    ),
                ),
                (
                    "user_id",
                    models.BigIntegerField(
                        error_messages={
                            "unique": "Пользователь с таким Телеграм ID уже существует"
                        },
                        null=True,
                        unique=True,
                        verbose_name="Телеграм ID",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "администратор",
                "verbose_name_plural": "администраторы",
                "ordering": ("id",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
