import logging
import os
import pathlib
import socket
from logging.handlers import RotatingFileHandler

import validators
from flask import Flask
from flask.logging import default_handler

from .discord_handler import DiscordHandler


class Logging:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        app_name = app.config.get("APP_NAME", app.logger.name)
        app_host = app.config.get("APP_HOST", socket.gethostname())
        app.logger.name = f"{app_name}@{app_host}"
        app_env = app.config.get("ENV_SET", None)

        # Formatter
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(pathname)s(%(lineno)s) %(message)s"
        )
        level = app.config.get("LOG_LEVEL", "INFO")

        # replace format
        default_handler.setFormatter(formatter)
        default_handler.setLevel(level)

        log_file = app.config.get("LOG_PATH_INFO")
        if log_file:
            pathlib.Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)
            # FileHandler Info
            file_handler = RotatingFileHandler(filename=log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level)
            app.logger.addHandler(file_handler)

        # Discord Log
        # Formatter
        discord_formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(pathname)s | %(lineno)s | %(message)s"
        )
        discord_level = app.config.get("LOG_DISCORD_LEVEL", "WARNING")

        discord_hook = app.config.get("LOG_DISCORD_HOOK_URL")
        if isinstance(discord_hook, str) and validators.url(discord_hook):
            discord_handler = DiscordHandler(
                service_name=app_name,
                environment=app_env,
                webhook_url=discord_hook,
            )
            discord_handler.setFormatter(discord_formatter)
            discord_handler.setLevel(discord_level)
            app.logger.addHandler(discord_handler)
