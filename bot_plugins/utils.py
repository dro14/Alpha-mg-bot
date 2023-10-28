from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_reply_markup(items):
    keyboard = []
    for item in items:
        button = InlineKeyboardButton(item, callback_data=item)
        keyboard.append([button])
    return InlineKeyboardMarkup(keyboard)


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
