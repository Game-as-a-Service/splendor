from typing import List

from flask_caching import Cache
from sqlalchemy.orm import Query, Session

from api.common.datetime_utils import date_to_str
from dbmodels.nike.buy_and_sell_date import BuyAndSellDate


class BacktestActionService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session

    def get_buy_and_sell_date(
            self,
            symbol: str,
            oriented: str,
            strategy: str,
            start_at: str = None,
            end_at: str = None
    ) -> List[BuyAndSellDate]:
        query: Query = self._nike_sql_session.query(BuyAndSellDate) \
            .filter(BuyAndSellDate.symbol == symbol) \
            .filter(BuyAndSellDate.oriented == oriented) \
            .filter(BuyAndSellDate.strategy == strategy)

        if not start_at or not end_at:
            return query.order_by(BuyAndSellDate.date.asc()).all()

        return query.filter(BuyAndSellDate.date.between(start_at, end_at)) \
            .order_by(BuyAndSellDate.date.asc()) \
            .all()

    def backtest_action(self, symbol: str, oriented: str, strategy: str, start_at: str, end_at: str) -> List[dict]:
        cache_key = self._backtest_action_cache_key(symbol, oriented, strategy, start_at, end_at)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        results: List[BuyAndSellDate] = self.get_buy_and_sell_date(symbol, oriented, strategy, start_at, end_at)

        data = []
        if not results:
            return data

        for r in results:
            data.append({
                "date": date_to_str(r.date),
                "action": r.action
            })

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _backtest_action_cache_key(symbol: str, oriented: str, strategy: str, start_at: str, end_at: str) -> str:
        return f"{symbol}_{oriented}_{strategy}_{start_at}_{end_at}_backtest_action"
