import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "Nike-Api-Flask"
    ENV_SET = "Local"
    DEBUG = True

    JSON_AS_ASCII = False
    SECRET_KEY = "Nike Flask Secret"

    # Growin Url
    GROWIN_URL = "https://127.0.0.1/"

    # Growin Mail Server
    GROWIN_MAIL_URL = "https://127.0.0.1/"

    # log setting
    LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'nike_error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'nike_info.log')
    LOG_PATH_DEBUG = os.path.join(LOG_PATH, 'nike_debug.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10

    # For Discord Log Channel
    LOG_DISCORD_HOOK_URL = "https://discord.com/api/webhooks/"
    LOG_DISCORD_LEVEL = "WARNING"

    # For Discord register TradingView Indicator Channel
    DISCORD_TRADINGVIEW_HOOK_URL = "https://discord.com/api/webhooks/"

    # CRONJOB SERVER
    CRONJOB_HOST = "127.0.0.1"
    CRONJOB_USER = ""
    CRONJOB_PWD = ""

    # MySQL and SQLAlchemy Setting
    # Manager DB
    MANAGER_DB_HOST = "127.0.0.1"
    MANAGER_DB_PORT = 3306
    MANAGER_DB_USER = "root"
    MANAGER_DB_PWD = "secret"
    MANAGER_DB_NAME = "tradingvalley_manager"

    # User Profile DB
    USER_DB_HOST = "127.0.0.1"
    USER_DB_PORT = 3306
    USER_DB_USER = "root"
    USER_DB_PWD = "secret"
    USER_DB_NAME = "user_profile"

    # Nike DB
    NIKE_DB_HOST = "127.0.0.1"
    NIKE_DB_PORT = 3306
    NIKE_DB_USER = "root"
    NIKE_DB_PWD = "secret"
    NIKE_DB_NAME = "nike"

    # Symbol DB
    SYMBOL_DB_HOST = "127.0.0.1"
    SYMBOL_DB_PORT = 3306
    SYMBOL_DB_USER = "root"
    SYMBOL_DB_PWD = "secret"
    SYMBOL_DB_NAME = "symboldb"

    # SEC13F DB
    SEC13F_DB_HOST = "127.0.0.1"
    SEC13F_DB_PORT = 3306
    SEC13F_DB_USER = "root"
    SEC13F_DB_PWD = "secret"
    SEC13F_DB_NAME = "SEC13Fdb"

    # Notification DB
    NOTICE_DB_HOST = "127.0.0.1"
    NOTICE_DB_PORT = 3306
    NOTICE_DB_USER = "root"
    NOTICE_DB_PWD = "secret"
    NOTICE_DB_NAME = "push_notification"

    MANAGER_DATABASE_URI = f"mysql+pymysql://{MANAGER_DB_USER}:{MANAGER_DB_PWD}@{MANAGER_DB_HOST}:{MANAGER_DB_PORT}/{MANAGER_DB_NAME}?charset=utf8mb4"  # noqa: E501
    USER_DATABASE_URI = f"mysql+pymysql://{USER_DB_USER}:{USER_DB_PWD}@{USER_DB_HOST}:{USER_DB_PORT}/{USER_DB_NAME}?charset=utf8mb4"  # noqa: E501
    NIKE_DATABASE_URI = f"mysql+pymysql://{NIKE_DB_USER}:{NIKE_DB_PWD}@{NIKE_DB_HOST}:{NIKE_DB_PORT}/{NIKE_DB_NAME}?charset=utf8mb4"  # noqa: E501
    SYMBOL_DATABASE_URI = f"mysql+pymysql://{SYMBOL_DB_USER}:{SYMBOL_DB_PWD}@{SYMBOL_DB_HOST}:{SYMBOL_DB_PORT}/{SYMBOL_DB_NAME}?charset=utf8mb4"  # noqa: E501
    SEC13F_DATABASE_URI = f"mysql+pymysql://{SEC13F_DB_USER}:{SEC13F_DB_PWD}@{SEC13F_DB_HOST}:{SEC13F_DB_PORT}/{SEC13F_DB_NAME}?charset=utf8mb4"  # noqa: E501
    NOTICE_DATABASE_URI = f"mysql+pymysql://{NOTICE_DB_USER}:{NOTICE_DB_PWD}@{NOTICE_DB_HOST}:{NOTICE_DB_PORT}/{NOTICE_DB_NAME}?charset=utf8mb4"  # noqa: E501
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800

    # Flask-Session Setting
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_KEY_PREFIX = f"{ENV_SET}-nike-session:"
    SESSION_REDIS_HOST = 'localhost'
    SESSION_REDIS_PASSWORD = "secret"
    SESSION_REDIS_PORT = '6379'
    SESSION_REDIS_DB = 9
    SESSION_REDIS_SSL = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=100)  # 配置10分鐘有效

    # Flask-Cache Setting
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = SESSION_REDIS_HOST
    CACHE_REDIS_PORT = SESSION_REDIS_PORT
    CACHE_REDIS_PASSWORD = SESSION_REDIS_PASSWORD
    CACHE_KEY_PREFIX = f"{ENV_SET}-nike-cache:"
    CACHE_DEFAULT_TIMEOUT = 4320
    CACHE_REDIS_DB = 10
    CACHE_THRESHOLD = 922337203685477580
    CACHE_OPTIONS = {
        'ssl': bool(SESSION_REDIS_SSL)
    }

    # Stripe Setting
    STRIPE_PUBLISHABLE_KEY = ""
    STRIPE_SECRET_KEY = ""
    STRIPE_WEBHOOK_SECRET_KEY = ""
    ENDPOINT_SECRET = ""

    # Line Webhook Setting
    LINE_CHANNEL_ACCESS_TOKEN = ""
    LINE_CHANNEL_SECRET = ""
