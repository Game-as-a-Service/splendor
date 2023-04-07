import os
import re
from unittest import TestCase

from flask import Flask
from flask.ctx import AppContext
from flask_caching.backends.base import BaseCache
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from api import create_app
from api.containers.services_container import ServicesContainer
from config.api_config import Config

TestCase.maxDiff = None


class BaseFlaskTestCase(TestCase):
    app: Flask
    app_context: AppContext
    container: ServicesContainer
    user_sql_session: Session
    nike_sql_session: Session
    symbol_sql_session: Session
    sec13f_sql_session: Session
    manager_sql_session: Session
    notice_sql_session: Session
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

        db_host_list = [Config.NIKE_DB_HOST, Config.SYMBOL_DB_HOST, Config.SEC13F_DB_HOST, Config.NOTICE_DB_HOST]
        for db_host in db_host_list:
            if db_host and not re.search(r'^\s*localhost\s*$|^\s*127.0.0.1\s*$', db_host):
                raise Exception('測試請使用本地端的資料庫')

        user_engine = create_engine(
            cls.app.config["USER_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.user_sql_session = sessionmaker(bind=user_engine, autocommit=True)()

        nike_engine = create_engine(
            cls.app.config["NIKE_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.nike_sql_session = sessionmaker(bind=nike_engine, autocommit=True)()

        symbol_engine = create_engine(
            cls.app.config["SYMBOL_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.symbol_sql_session = sessionmaker(bind=symbol_engine, autocommit=True)()

        sec13f_engine = create_engine(
            cls.app.config["SEC13F_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.sec13f_sql_session = sessionmaker(bind=sec13f_engine, autocommit=True)()

        manager_engine = create_engine(
            cls.app.config["MANAGER_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.manager_sql_session = sessionmaker(bind=manager_engine, autocommit=True)()

        notice_engine = create_engine(
            cls.app.config["NOTICE_DATABASE_URI"],
            pool_size=cls.app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=cls.app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=cls.app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )
        cls.notice_sql_session = sessionmaker(bind=notice_engine, autocommit=True)()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.nike_sql_session:
            cls.nike_sql_session.close_all()

        if cls.symbol_sql_session:
            cls.symbol_sql_session.close_all()

        if cls.sec13f_sql_session:
            cls.sec13f_sql_session.close_all()

        if cls.user_sql_session:
            cls.user_sql_session.close_all()

        if cls.manager_sql_session:
            cls.manager_sql_session.close_all()

        if cls.notice_sql_session:
            cls.notice_sql_session.close_all()

        cls.cache.clear()

        setattr(cls, "app", None)
        setattr(cls, "app_context", None)
        setattr(cls, "container", None)
        setattr(cls, 'nike_sql_session', None)
        setattr(cls, 'symbol_sql_session', None)
        setattr(cls, 'user_sql_session', None)
        setattr(cls, 'sec13f_sql_session', None)
        setattr(cls, 'manager_sql_session', None)
        setattr(cls, 'notice_sql_session', None)
        setattr(cls, 'cache', None)

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
