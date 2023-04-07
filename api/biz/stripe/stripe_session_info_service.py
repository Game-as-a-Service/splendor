from sqlalchemy.orm import Session

from dbmodels.user_profile.stripe_session_info import StripeSessionInfo


class StripeSessionInfoService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get(self, key: str, value: str) -> StripeSessionInfo:
        return self._user_sql_session.query(StripeSessionInfo) \
            .filter(getattr(StripeSessionInfo, key) == value) \
            .first()

    def insert(self, data: dict) -> None:
        self._user_sql_session.add(StripeSessionInfo(**data))
        self._user_sql_session.flush()

    def update(self, key: str, value: str, data: dict) -> None:
        self._user_sql_session.query(StripeSessionInfo) \
            .filter(getattr(StripeSessionInfo, key) == value) \
            .update(data)
