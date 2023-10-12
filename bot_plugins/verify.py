from alpha.models import User, CustomUser
from pyrogram import filters


async def found_match(users, update, attr1, attr2):
    for user in users:
        if getattr(user, attr1) == getattr(update.from_user, attr1):
            if not user.user_id:
                user.user_id = update.from_user.id
                if getattr(update.from_user, attr2):
                    setattr(user, attr2, getattr(update.from_user, attr2))
                await user.save()
            return True


async def func(_, __, update):
    if update.from_user.username or update.from_user.phone_number:
        for model in [CustomUser, User]:
            users = await model.objects.all()
            if update.from_user.username:
                if await found_match(users, update, "username", "phone_number"):
                    return True
            if update.from_user.phone_number:
                if await found_match(users, update, "phone_number", "username"):
                    return True

    await update.reply("Вы не зарегистрированы в системе")
    return False


verify = filters.create(func)
