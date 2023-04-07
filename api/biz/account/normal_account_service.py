import uuid
from typing import Optional

from flask import session
from sqlalchemy.orm import Session

from api.biz.error import InvalidInvocation
from api.common.datetime_utils import date_to_str
from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo


class NormalAccountService:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    def get_customer_info_by_user_id(self, user_id: str) -> NikeCustomerInfo:
        return self._user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.user_id == user_id) \
            .first()

    def modify_watchlist_index_by_user_id(self, user_id: str, watchlist_index: int):
        self._user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.user_id == user_id) \
            .update({"watchlist_index": watchlist_index})

    def get_user(self, user_id: str) -> Optional[dict]:
        cus_info: NikeCustomerInfo = self.get_customer_info_by_user_id(user_id)

        if not cus_info:
            return None

        subscribed = False
        if cus_info.status in ["active", "trialing", "canceled"]:
            subscribed = True

        return {
            "subscribed": subscribed,
            "plan": cus_info.plan,
            "subscribedAt": date_to_str(cus_info.subscribed_at),
            "expireAt": date_to_str(cus_info.expire_at),
            "watchlist": cus_info.watchlist,
            "watchlistIdx": cus_info.watchlist_index
        }

    def add_user(self, user_id: str, email: str):
        self._user_sql_session.add(NikeCustomerInfo(**{
            "user_id": user_id,
            "plan": "Free",
            "email": email,
            "status": "inactive",
            "watchlist": [
                {
                    "watchlistId": str(uuid.uuid4().hex),
                    "name": "我的追蹤清單",
                    "symbols": [],
                }
            ],
            "use_tag": True
        }))
        self._user_sql_session.flush()

    def get_user_subscription_plan(self, user_id: str) -> dict:
        cus_info: NikeCustomerInfo = self.get_customer_info_by_user_id(user_id)

        if not cus_info:
            raise InvalidInvocation(f"user_id ({user_id}) 不存在.")

        if cus_info.plan not in ["Free", "Basic Monthly", "Basic Yearly", "Premium Monthly", "Premium Yearly"]:
            raise InvalidInvocation(f"plan ({cus_info.plan}) 不在指定範圍內.")

        return {"plan": cus_info.plan}

    def line_account_link(self, nonce: str):
        self._user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.user_id == session["user_id"]) \
            .update({"line_nonce": nonce})

    def get_line_account_link_status(self) -> dict:
        cus_info: NikeCustomerInfo = self.get_customer_info_by_user_id(session["user_id"])
        if not cus_info:
            raise InvalidInvocation(f"user_id ({session['user_id']}) 不存在.")

        return {"status": cus_info.line_bind_status}
