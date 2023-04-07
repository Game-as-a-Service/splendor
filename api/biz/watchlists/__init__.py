from logging import Logger
from typing import Dict, List

from flask import session

from api.biz.error import InvalidInvocation, TenantDataConflictError
from api.biz.watchlists._base import WatchlistHandler
from api.biz.watchlists._business import BusinessHandler
from api.biz.watchlists._normal import NormalHandler


class WatchlistServiceFacade:
    _handlers: Dict[str, WatchlistHandler]

    def __init__(self, logger: Logger):
        self._logger = logger
        self._handlers = {
            r.account_type: r
            for r in [
                BusinessHandler(),
                NormalHandler()
            ]
        }

    @staticmethod
    def valid_identity(plan: str) -> None:
        if plan in ["Guest"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

    def add_watchlist(self, account_type: str, user_id: str, name: str) -> str:
        return self._handler(account_type).add_watchlist(user_id, name)

    def delete_watchlist(self, account_type: str, user_id: str, watchlist_id: str) -> None:
        return self._handler(account_type).delete_watchlist(user_id, watchlist_id)

    def rename_watchlist(self, account_type: str, user_id: str, watchlist_id: str, name: str) -> None:
        return self._handler(account_type).rename_watchlist(user_id, watchlist_id, name)

    def add_symbol(self, account_type: str, user_id: str, watchlist_id: str, symbol: str) -> None:
        return self._handler(account_type).add_symbol(user_id, watchlist_id, symbol)

    def remove_symbol(self, account_type: str, user_id: str, watchlist_id: str, symbol: str) -> None:
        return self._handler(account_type).remove_symbol(user_id, watchlist_id, symbol)

    def replace_symbols(self, account_type: str, user_id: str, watchlist_id: str, symbols: List[str]) -> None:
        return self._handler(account_type).replace_symbols(user_id, watchlist_id, symbols)

    def _handler(self, account_type: str) -> WatchlistHandler:
        if account_type not in self._handlers:
            raise InvalidInvocation(
                f"錯誤的 account type {account_type},"
                f"account type 必須是 {list(self._handlers.keys())} 其中之一")

        return self._handlers[account_type]
