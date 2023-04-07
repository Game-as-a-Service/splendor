from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class UserDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["USER_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.userDBSession = scoped_session(session_local)


class NikeDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["NIKE_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.nikeDBSession = scoped_session(session_local)


class SymbolDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["SYMBOL_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.symbolDBSession = scoped_session(session_local)


class SEC13FDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["SEC13F_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.sec13FDBSession = scoped_session(session_local)


class ManagerDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["MANAGER_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.managerDBSession = scoped_session(session_local)


class NoticeDBSession:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def init_app(app: Flask):
        engine = create_engine(
            app.config["NOTICE_DATABASE_URI"],
            pool_size=app.config["SQLALCHEMY_POOL_SIZE"],
            pool_recycle=app.config["SQLALCHEMY_POOL_RECYCLE"],
            pool_timeout=app.config["SQLALCHEMY_POOL_TIMEOUT"],
            encoding="utf8",
            pool_pre_ping=True
        )

        session_local = sessionmaker(bind=engine, autocommit=True)
        app.noticeDBSession = scoped_session(session_local)
