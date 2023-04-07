from typing import List

from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session, Query

from api.common.number_utils import decimal_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.symbol_historical_dividend_info import SymbolHistoricalDividendInfo


class HistoricalDividendService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            updated_at_utils: UpdatedAtUtils
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._updated_at_utils = updated_at_utils

    def get_symbol_historical_dividend_info(self, symbol: str, nums: int = 0) -> List[SymbolHistoricalDividendInfo]:
        query: Query = self._nike_sql_session.query(SymbolHistoricalDividendInfo) \
            .filter(SymbolHistoricalDividendInfo.symbol == symbol) \
            .order_by(SymbolHistoricalDividendInfo.year.desc())

        if nums == 0:
            return query.all()
        return query.limit(nums).all()

    def dividend_info(self, symbol: str, nums: int) -> dict:
        cache_key = self._dividend_info_cache_key(session["plan"], symbol, nums)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        infos: List[SymbolHistoricalDividendInfo] = self.get_symbol_historical_dividend_info(symbol, nums)
        updated_at = self._updated_at_utils.get_date("nike", "symbol_historical_dividend_info")

        if not infos:
            return {
                "isEmpty": True,
                "updatedAt": updated_at,
                "dividendInfo": []
            }

        tmp = []
        is_empty = True
        for i in infos:
            if i.cash_dividend or i.stock_dividend or i.total_dividend or i.filled_days or \
                    i.dividend_yield and i.eps and i.payout_ratio:
                is_empty = False

            if session["plan"] in ["Guest", "Free"]:
                tmp.append({
                    "year": i.year,
                    "cashDividend": decimal_to_float(i.cash_dividend),
                    "stockDividend": decimal_to_float(i.stock_dividend),
                    "totalDividend": decimal_to_float(i.total_dividend),
                    "filledDays": "lock",
                    "dividendYield": decimal_to_float(i.dividend_yield),
                    "eps": decimal_to_float(i.eps),
                    "payoutRatio": decimal_to_float(i.payout_ratio)
                })
                continue

            tmp.append({
                "year": i.year,
                "cashDividend": decimal_to_float(i.cash_dividend),
                "stockDividend": decimal_to_float(i.stock_dividend),
                "totalDividend": decimal_to_float(i.total_dividend),
                "filledDays": i.filled_days,
                "dividendYield": decimal_to_float(i.dividend_yield),
                "eps": decimal_to_float(i.eps),
                "payoutRatio": decimal_to_float(i.payout_ratio)
            })

        data = {
            "isEmpty": is_empty,
            "updatedAt": updated_at,
            "dividendInfo": tmp
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _dividend_info_cache_key(plan: str, symbol: str, nums: int) -> str:
        return f"{plan}_{symbol}_{nums}_dividend_info"
