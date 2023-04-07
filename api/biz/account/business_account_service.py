import hashlib
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from api.biz.error import InvalidInvocation
from api.common.datetime_utils import date_to_str
from dbmodels.user_profile.business_account import BusinessAccount


class BusinessAccountService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get_business_account_by_user_id_and_password(self, user_id: str, password: str) -> BusinessAccount:
        return self._user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == user_id) \
            .filter(BusinessAccount.password == password) \
            .first()

    def get_business_account_by_user_id(self, user_id: str) -> BusinessAccount:
        return self._user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == user_id) \
            .first()

    def modify_watchlist_index_by_user_id(self, user_id: str, watchlist_index):
        self._user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == user_id) \
            .update({"watchlist_index": watchlist_index})

    def get_user(self, user_id: str, password: str) -> Optional[dict]:
        user: BusinessAccount = self.get_business_account_by_user_id_and_password(user_id, password)
        if not user or not user.status:
            return None

        return {
            "subscribed": user.status,
            "plan": user.plan,
            "subscribedAt": date_to_str(user.subscribed_at),
            "expireAt": date_to_str(user.expire_at),
            "watchlist": user.watchlist
        }

    def get_user_by_user_id(self, user_id: str) -> Optional[dict]:
        user: BusinessAccount = self.get_business_account_by_user_id(user_id)
        if not user:
            return None

        return {
            "subscribed": user.status,
            "plan": user.plan,
            "subscribedAt": date_to_str(user.subscribed_at),
            "expireAt": date_to_str(user.expire_at),
            "watchlist": user.watchlist,
            "watchlistIdx": user.watchlist_index
        }

    def generate_business_account(
            self,
            user_id: str,
            password: str,
            company: str,
            company_code: str,
            plan: str,
            subscribed_at: str,
            expire_at: str
    ) -> None:
        user: BusinessAccount = self.get_business_account_by_user_id(user_id)

        if user:
            raise InvalidInvocation(f"{user_id} is already exist.")

        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self._user_sql_session.add(BusinessAccount(**{
            "user_id": user_id,
            "password": password,
            "company": company,
            "company_code": company_code,
            "status": True,
            "plan": plan,
            "subscribed_at": subscribed_at,
            "expire_at": expire_at,
            "watchlist": [
                {
                    "watchlistId": str(uuid.uuid4().hex),
                    "name": "我的追蹤清單",
                    "symbols": [],
                }
            ],
        }))
        self._user_sql_session.flush()
