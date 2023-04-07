from sqlalchemy.orm import Session

from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo


class NikeCustomerInfoService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get(self, key: str, value: str) -> NikeCustomerInfo:
        return self._user_sql_session.query(NikeCustomerInfo) \
            .filter(getattr(NikeCustomerInfo, key) == value) \
            .first()

    def update(self, key: str, value: str, data: dict) -> None:
        self._user_sql_session.query(NikeCustomerInfo) \
            .filter(getattr(NikeCustomerInfo, key) == value) \
            .update(data)
