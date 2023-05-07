import os
import re
from unittest import TestCase

from flask import Flask
from flask.ctx import AppContext
from flask_caching.backends.base import BaseCache
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config.api_config import Config
from interface.api import create_app
from interface.api.containers.services_container import ServicesContainer

TestCase.maxDiff = None


class BaseFlaskTestCase(TestCase):
    app: Flask
    app_context: AppContext
    container: ServicesContainer
    user_sql_session: Session

    cache: BaseCache

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tests_path = os.path.realpath(os.path.dirname(__file__))
        self.fixtures_path = os.path.join(self.tests_path, "file_fixtures")

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.app: Flask = create_app()
        cls.app.testing = True
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.app.logger.setLevel("ERROR")
        cls.container = cls.app.extensions["container"]
        cls.cache: BaseCache = cls.container.provide("cache")
        cls.cache.clear()

        user_engine = create_engine(
            cls.app.config["USER_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True,
        )
        cls.user_sql_session = sessionmaker(bind=user_engine, autocommit=True)()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.user_sql_session:
            cls.user_sql_session.close_all()

        cls.cache.clear()

        setattr(cls, "app", None)
        setattr(cls, "app_context", None)
        setattr(cls, "container", None)

        setattr(cls, "user_sql_session", None)

        setattr(cls, "cache", None)

    def setUp(self) -> None:
        # playerA 有4黑token, 0分
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
