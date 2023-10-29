from alpha.models import User, CustomUser
from asgiref.sync import sync_to_async
from pyrogram import filters


def found_match(users, update, attr1, attr2):
    for user in users:
        if getattr(user, attr1) == getattr(update.from_user, attr1):
            if user.user_id != update.from_user.id:
                user.user_id = update.from_user.id
                if getattr(update.from_user, attr2):
                    setattr(user, attr2, getattr(update.from_user, attr2))
                user.save()
            return True


def is_in(user, users):
    for u in users:
        if user.id == u.user_id:
            return True
    return False


afound_match = sync_to_async(found_match)
ais_in = sync_to_async(is_in)


async def is_registered(_, client, update):
    if update.from_user.username or update.from_user.phone_number:
        for model in [CustomUser, User]:
            users = model.objects.all()
            if update.from_user.username:
                if await afound_match(users, update, "username", "phone_number"):
                    return True
            if update.from_user.phone_number:
                if await afound_match(users, update, "phone_number", "username"):
                    return True

    await client.send_message(update.from_user.id, "Вы не зарегистрированы в системе")
    return False


async def is_admin_verbose(_, client, update):
    admins = User.objects.all()
    if await ais_in(update.from_user, admins):
        return True

    await client.send_message(update.from_user.id, "Вы не являетесь администратором")
    return False


async def is_sender_verbose(_, client, update):
    senders = CustomUser.objects.filter(
        type__in=["Отправитель", "Отправитель и Получатель"]
    )
    if await ais_in(update.from_user, senders):
        return True

    await client.send_message(update.from_user.id, "Вы не являетесь отправителем")
    return False


async def is_receiver_verbose(_, client, update):
    receivers = CustomUser.objects.filter(
        type__in=["Получатель", "Отправитель и Получатель"]
    )
    if await ais_in(update.from_user, receivers):
        return True

    await client.send_message(update.from_user.id, "Вы не являетесь получателем")
    return False


async def is_admin(_, __, update):
    admins = User.objects.all()
    return await ais_in(update.from_user, admins)


async def is_sender(_, __, update):
    senders = CustomUser.objects.filter(
        type__in=["Отправитель", "Отправитель и Получатель"]
    )
    return await ais_in(update.from_user, senders)


async def is_receiver(_, __, update):
    receivers = CustomUser.objects.filter(
        type__in=["Получатель", "Отправитель и Получатель"]
    )
    return await ais_in(update.from_user, receivers)


registered = filters.create(is_registered)
admin_verbose = filters.create(is_admin_verbose)
sender_verbose = filters.create(is_sender_verbose)
receiver_verbose = filters.create(is_receiver_verbose)
admin = filters.create(is_admin)
sender = filters.create(is_sender)
receiver = filters.create(is_receiver)
