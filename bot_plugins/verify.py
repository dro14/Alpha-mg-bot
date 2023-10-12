from alpha.models import User, CustomUser
from asgiref.sync import sync_to_async
from pyrogram import filters


def found_match(users, update, attr1, attr2):
    for user in users:
        if getattr(user, attr1) == getattr(update.from_user, attr1):
            if user.user_id != update.from_user.id:
                user.user_id = update.from_user.id
                if getattr(user, attr2) != getattr(update.from_user, attr2):
                    setattr(user, attr2, getattr(update.from_user, attr2))
                user.save()
            return True


afound_match = sync_to_async(found_match)


async def func(_, client, update):
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


verify = filters.create(func)
