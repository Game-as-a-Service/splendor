from flask import Flask
from flask_caching import Cache


class RedisCache:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        cache_config = {
            "CACHE_TYPE": None,
            "CACHE_REDIS_HOST": None,
            "CACHE_REDIS_PORT": None,
            "CACHE_REDIS_PASSWORD": None,
            "CACHE_KEY_PREFIX": None,
            "CACHE_DEFAULT_TIMEOUT": None,
            "CACHE_REDIS_DB": None,
            "CACHE_THRESHOLD": None,
        }

        for key in cache_config:
            if cache_config[key]:
                continue

            if not app.config.get(key):
                raise Exception(f"Redis config 缺少 {key}, 請確認 config/api_config.py")
            cache_config[key] = app.config.get(key)

        cache = Cache(app, config=cache_config)
        app.rediscache = cache
