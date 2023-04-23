import uuid
from typing import Optional

from flask import session
from sqlalchemy.orm import Session

from dbmodels.user_profile.user_info import UserInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation


class UserInfoService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get_user_info_by_user_id(self, user_id: str) -> UserInfo:
        return (
            self._user_sql_session.query(UserInfo)
            .filter(UserInfo.user_id == user_id)
            .first()
        )

    def modify_user_info_by_user_id(self, user_id: str, name: str) -> None:
        self._user_sql_session.query(UserInfo).filter(
            UserInfo.user_id == user_id
        ).update({"name": name})

    def add_user_info(self, user_id: str, name: str):
        self._user_sql_session.add(
            UserInfo(
                **{
                    "user_id": user_id,
                    "name": name,
                }
            )
        )
        self._user_sql_session.flush()
