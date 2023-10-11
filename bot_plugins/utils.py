def iterate_check(users, message):
    for user in users:
        if message.from_user.username == user.username:
            if not user.user_id:
                user.user_id = message.from_user.id
                user.phone_number = message.from_user.phone_number
                user.save()
            return True
        if message.from_user.phone_number == user.phone_number:
            if not user.user_id:
                user.user_id = message.from_user.id
                user.username = message.from_user.username
                user.save()
            return True
