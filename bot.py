import time

time.sleep(5)

from alpha.models import CustomUser
from pyrogram import Client, filters
import os


app = Client(
    "my_account",
    api_id=os.environ["API_ID"],
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"],
)


@app.on_message(filters.incoming & filters.private & filters.text)
def handle_text(client, message):
    if message.text == "/users":
        users = CustomUser.objects.all()
        reply = ""
        for i, user in enumerate(users):
            reply += f"{i+1}. {user.username}\n"
        message.reply_text(reply)
    else:
        message.reply_text(message.text)


if __name__ == "__main__":
    app.run()
