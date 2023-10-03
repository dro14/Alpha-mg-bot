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
    message.reply_text(message.text)
