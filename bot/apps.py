from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"
    verbose_name = "Pyrogram Bot"

    pyrogram_client = None

    @classmethod
    def get_app(cls):
        return cls.pyrogram_client

    def ready(self):
        from django.conf import settings
        from pyrogram import Client
        from pyrogram.enums import ParseMode

        bot_settings = settings.PYROGRAM_BOT

        client = Client(
            name=bot_settings["BOT_NAME"],
            api_id=bot_settings["API_ID"],
            api_hash=bot_settings["API_HASH"],
            bot_token=bot_settings["BOT_TOKEN"],
            sleep_threshold=15,
            parse_mode=ParseMode.MARKDOWN,
            plugins={"root": "bot_plugins"},
        )

        BotConfig.pyrogram_client = client
