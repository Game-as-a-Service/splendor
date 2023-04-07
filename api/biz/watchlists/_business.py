import uuid
from typing import List

from sqlalchemy.orm import Session

from api.biz.account.business_account_service import BusinessAccountService
from api.biz.error import DataNotFound
from api.biz.watchlists._base import WatchlistHandler
from api.containers.decorator import inject_service
from dbmodels.user_profile.business_account import BusinessAccount


class BusinessHandler(WatchlistHandler):

    @property
    def account_type(self) -> str:
        return 'business'

    @inject_service()
    def __init__(self, user_sql_session: Session, business_account_service: BusinessAccountService):
        super().__init__()
        self._user_sql_session = user_sql_session
        self._business_account_service = business_account_service

    def _get_business_account_by_user_id(self, user_id: str) -> BusinessAccount:
        return self._user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == user_id) \
            .first()

    def _update_watchlist(self, user_id: str, watchlist: list) -> None:
        self._user_sql_session.query(BusinessAccount) \
            .filter(BusinessAccount.user_id == user_id) \
            .update({"watchlist": watchlist})

    def add_watchlist(self, user_id: str, name: str) -> str:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist

        watchlist_id = str(uuid.uuid4().hex)
        watchlist.append(
            {
                "watchlistId": watchlist_id,
                "name": name,
                "symbols": []
            }
        )
        self._update_watchlist(user_id, watchlist)
        return watchlist_id

    def delete_watchlist(self, user_id: str, watchlist_id: str) -> None:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist
        tmp = None
        for w in watchlist:
            if w["watchlistId"] == watchlist_id:
                tmp = w

        if tmp is None:
            return

        watchlist.remove(tmp)
        self._update_watchlist(user_id, watchlist)
        self._business_account_service.modify_watchlist_index_by_user_id(user_id, 0)

    def rename_watchlist(self, user_id: str, watchlist_id: str, name: str) -> None:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist
        for w in watchlist:
            if w["watchlistId"] == watchlist_id:
                w["name"] = name

        self._update_watchlist(user_id, watchlist)

    def add_symbol(self, user_id: str, watchlist_id: str, symbol: str) -> None:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist
        for w in watchlist:
            if w["watchlistId"] == watchlist_id:
                if symbol in w["symbols"]:
                    return
                w["symbols"].append(symbol)

        self._update_watchlist(user_id, watchlist)

    def remove_symbol(self, user_id: str, watchlist_id: str, symbol: str) -> None:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist
        for w in watchlist:
            if w["watchlistId"] == watchlist_id:
                if symbol not in w["symbols"]:
                    return
                w["symbols"].remove(symbol)

        self._update_watchlist(user_id, watchlist)

    def replace_symbols(self, user_id: str, watchlist_id: str, symbols: List[str]) -> None:
        user: BusinessAccount = self._get_business_account_by_user_id(user_id)
        if not user:
            raise DataNotFound(f"user_id ({user_id}) is invalid user.")

        watchlist = user.watchlist
        for w in watchlist:
            if w["watchlistId"] == watchlist_id:
                w["symbols"] = symbols

        self._update_watchlist(user_id, watchlist)
