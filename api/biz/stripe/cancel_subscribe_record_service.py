from sqlalchemy.orm import Session

from dbmodels.user_profile.cancel_subscribe_record import CancelSubscribeRecord


class CancelSubscribeRecordService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def insert(self, data: dict) -> None:
        self._user_sql_session.add(CancelSubscribeRecord(**data))
        self._user_sql_session.flush()
