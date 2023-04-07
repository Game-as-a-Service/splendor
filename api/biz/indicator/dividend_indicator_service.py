from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.error import DataNotFound
from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.common.number_utils import decimal_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.symbol_dividend_info import SymbolDividendInfo
from dbmodels.nike.symbol_info import SymbolInfo


class DividendIndicatorService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            symbol_info_service: SymbolInfoService,
            updated_at_utils: UpdatedAtUtils,
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._symbol_info_service = symbol_info_service
        self._updated_at_utils = updated_at_utils

    def get_symbol_dividend_info_by_symbol(self, symbol: str) -> SymbolDividendInfo:
        return self._nike_sql_session.query(SymbolDividendInfo) \
            .filter(SymbolDividendInfo.symbol == symbol) \
            .first()

    def dividend_indicator(self, symbol: str) -> dict:
        cache_key = self._dividend_indicator_cache_key(session["plan"], symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol_info: SymbolInfo = self._symbol_info_service.get_symbol_info_by_symbol(symbol)
        if not symbol_info:
            raise DataNotFound("找不到指定的Symbol")

        data = {
            "updatedAt": self._updated_at_utils.get_date("nike", "symbol_dividend_info"),
            "symbol": self._create_dividend_info(symbol),
            "sameIndustry": self._create_dividend_info(symbol_info.main_category),
            "allMarket": self._create_dividend_info("ALL_MARKET")
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _dividend_indicator_cache_key(plan: str, symbol: str) -> str:
        return f"{plan}_{symbol}_dividend_indicator"

    def _create_dividend_info(self, symbol: str) -> dict:
        dividend_info: SymbolDividendInfo = self.get_symbol_dividend_info_by_symbol(symbol)
        if not dividend_info:
            return {
                "dividendYield": None,
                "filledDays": None,
                "filledRatio": None,
                "volatility": None,
                "continuousYear": None
            }

        if session["plan"] in ["Guest", "Free"]:
            return {
                "dividendYield": decimal_to_float(dividend_info.dividend_yield),
                "filledDays": "lock",
                "filledRatio": "lock",
                "volatility": decimal_to_float(dividend_info.volatility),
                "continuousYear": dividend_info.continuous_year
            }

        return {
            "dividendYield": decimal_to_float(dividend_info.dividend_yield),
            "filledDays": decimal_to_float(dividend_info.filled_days),
            "filledRatio": decimal_to_float(dividend_info.filled_ratio),
            "volatility": decimal_to_float(dividend_info.volatility),
            "continuousYear": dividend_info.continuous_year
        }
