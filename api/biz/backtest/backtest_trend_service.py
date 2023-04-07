from decimal import Decimal
from typing import List

from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.reward_of_trend_period import RewardOfTrendPeriod


class BacktestTrendService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            symbol_service: SymbolService,
            updated_at_utils: UpdatedAtUtils
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._symbol_service = symbol_service
        self._updated_at_utils = updated_at_utils

    def get_reward_of_trend_period(self, symbol: str) -> List[RewardOfTrendPeriod]:
        return self._nike_sql_session.query(RewardOfTrendPeriod) \
            .filter(RewardOfTrendPeriod.symbol == symbol) \
            .order_by(RewardOfTrendPeriod.score.asc()) \
            .all()

    def trend_performance(self, symbol: str) -> dict:
        cache_key = self._trend_performance_cache_key(session["plan"], symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        results: List[RewardOfTrendPeriod] = self.get_reward_of_trend_period(symbol)
        if not results:
            return {
                "scoreList": [],
                "updatedAt": None,
                "startAt": None,
                "endAt": None
            }

        updated_at = self._updated_at_utils.get_date("nike", "reward_of_trend_period")

        tmp = []
        for r in results:
            if session["plan"] in ["Guest", "Free"] and r.score in [3, 4, 5]:
                tmp.append({
                    "score": r.score,
                    "occurrence": "lock",
                    "avgProfitAndLoss": "lock",
                    "profits": "lock",
                    "profitability": "lock",
                    "avgProfit": "lock",
                    "losses": "lock",
                    "lossRatio": "lock",
                    "avgLoss": "lock",
                    "avgHoldingTime": "lock"
                })
                continue

            losses = None
            if r.occurrence is not None and r.profits is not None:
                losses = r.occurrence - r.profits

            loss_ratio = None
            if r.profitability is not None:
                loss_ratio = decimal_to_float(Decimal(1) - r.profitability)

            tmp.append({
                "score": r.score,
                "occurrence": r.occurrence,
                "avgProfitAndLoss": decimal_to_float(r.avg_profit_and_loss),
                "profits": r.profits,
                "profitability": decimal_to_float(r.profitability),
                "avgProfit": decimal_to_float(r.avg_profit),
                "losses": losses,
                "lossRatio": loss_ratio,
                "avgLoss": decimal_to_float(r.avg_loss),
                "avgHoldingTime": decimal_to_float(r.avg_holding_time)
            })

        start_at, end_at = self._symbol_service.symbol_price_start_date_and_end_date(symbol)
        data = {
            "scoreList": tmp,
            "startAt": date_to_str(start_at, "%Y/%m"),
            "endAt": date_to_str(end_at, "%Y/%m"),
            "updatedAt": updated_at
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _trend_performance_cache_key(plan: str, symbol: str) -> str:
        return f"{plan}_{symbol}_trend_performance"
