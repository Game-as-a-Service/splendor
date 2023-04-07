from sqlalchemy.orm import Session

from dbmodels.user_profile.stripe_subscribe_info import StripeSubscribeInfo


class StripeSubscribeInfoService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get(self, key: str, value: str) -> StripeSubscribeInfo:
        return self._user_sql_session.query(StripeSubscribeInfo) \
            .filter(getattr(StripeSubscribeInfo, key) == value) \
            .order_by(StripeSubscribeInfo.created_at.desc()) \
            .first()

    def insert(self, data: dict) -> None:
        self._user_sql_session.add(StripeSubscribeInfo(**data))
        self._user_sql_session.flush()
