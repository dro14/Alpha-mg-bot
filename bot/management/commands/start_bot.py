from django.core.management.base import BaseCommand
from bot.apps import BotConfig


class Command(BaseCommand):
    def handle(self, *args, **options):
        app = BotConfig.get_app()

        if app is None:
            print("bot was not initialized")
            exit(127)

        app.run()
