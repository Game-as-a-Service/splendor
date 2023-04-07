from logging import Logger
from typing import List, Union, Optional

from flask import session
from flask_caching import Cache
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.biz.error import DataNotFound
from api.biz.symbol import SECTOR
from api.biz.symbol.symbol_service import SymbolService
from api.common.number_utils import decimal_to_float
from dbmodels.nike.recent_performance import RecentPerformance
from dbmodels.nike.symbol_info import SymbolInfo
from dbmodels.nike.top10_related_symbol import Top10RelatedSymbol


class SymbolInfoService:
    def __init__(
            self,
            cache: Cache,
            logger: Logger,
            symbol_service: SymbolService,
            nike_sql_session: Session
    ):
        self._cache = cache
        self._logger = logger
        self._symbol_service = symbol_service
        self._nike_sql_session = nike_sql_session

    def get_symbol_info_by_symbol(self, symbol: Union[str, List[str]]) -> Union[SymbolInfo, List[SymbolInfo]]:
        if isinstance(symbol, List):
            return self._nike_sql_session.query(SymbolInfo) \
                .filter(SymbolInfo.symbol.in_(symbol)) \
                .all()

        return self._nike_sql_session.query(SymbolInfo) \
            .filter(SymbolInfo.symbol == symbol) \
            .first()

    def get_recent_performance_by_symbol(self, symbol: str) -> RecentPerformance:
        return self._nike_sql_session.query(RecentPerformance) \
            .filter(RecentPerformance.symbol == symbol) \
            .first()

    def get_related_symbol_by_symbol(self, symbol: str) -> List[Top10RelatedSymbol]:
        return self._nike_sql_session.query(Top10RelatedSymbol) \
            .filter(Top10RelatedSymbol.symbol == symbol) \
            .order_by(Top10RelatedSymbol.correlation.desc()) \
            .all()

    def get_all_symbol(self, oriented: Optional[str] = None) -> List[SymbolInfo]:
        if not oriented:
            return self._nike_sql_session.query(SymbolInfo).all()

        return self._nike_sql_session.query(SymbolInfo) \
            .filter(getattr(SymbolInfo, oriented).in_([1, 2, 3, 4, 5])) \
            .all()

    def online_symbols(self, oriented: Optional[str] = None) -> List[str]:
        symbols: List[SymbolInfo] = self.get_all_symbol(oriented)
        return [r.symbol for r in symbols]

    def symbol_info(self, symbol: str) -> dict:
        cache_key = self._symbol_info_cache_key(symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol_info: SymbolInfo = self.get_symbol_info_by_symbol(symbol)
        if not symbol_info:
            raise DataNotFound(f"找不到指定的Symbol -> {symbol}")

        data = {
            "name": symbol_info.name,
            "exchange": symbol_info.exchange,
            "country": symbol_info.country,
            "value": symbol_info.value,
            "trend": symbol_info.trend,
            "swing": symbol_info.swing,
            "chip": symbol_info.chip,
            "dividend": symbol_info.dividend,
            "summary": symbol_info.summary,
            "mainCategory": symbol_info.main_category,
            "mainCategoryZhTw": symbol_info.main_category_zh_tw,
            "subCategory": symbol_info.sub_category,
            "subCategoryZhTw": symbol_info.sub_category_zh_tw,
            "marketCap": decimal_to_float(symbol_info.market_cap),
            "volume": decimal_to_float(symbol_info.volume),
            "volume20MA": decimal_to_float(symbol_info.volume_20MA),
            "symbol": self._get_recent_performance(symbol),
            "sameIndustry": self._get_recent_performance(symbol_info.main_category),
            "S&P500": self._get_recent_performance("S&P500")
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    def _get_recent_performance(self, symbol: str) -> dict:
        recent: RecentPerformance = self.get_recent_performance_by_symbol(symbol)
        if not recent:
            return {
                "OneDayReturn": None,
                "OneMonthReturn": None,
                "ThreeMonthsReturn": None,
                "HalfYearReturn": None,
                "OneYearReturn": None
            }

        return {
            "OneDayReturn": decimal_to_float(recent._1d_return),
            "OneMonthReturn": decimal_to_float(recent._1m_return),
            "ThreeMonthsReturn": decimal_to_float(recent._3m_return),
            "HalfYearReturn": decimal_to_float(recent._6m_return),
            "OneYearReturn": decimal_to_float(recent._1y_return)
        }

    @staticmethod
    def _symbol_info_cache_key(symbol: str) -> str:
        return f"{symbol}_symbol_info"

    def related_symbol(self, symbol: str) -> List[dict]:
        cache_key = self._related_symbol_cache_key(session["plan"], symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbols: List[Top10RelatedSymbol] = self.get_related_symbol_by_symbol(symbol)

        data = []
        for idx, s in enumerate(symbols):
            symbol_info: SymbolInfo = self.get_symbol_info_by_symbol(s.related_symbol)
            if not symbol_info:
                self._logger.error(f"找不到指定的Symbol -> {s.related_symbol}")
                continue

            if session["plan"] in ["Guest", "Free"] and idx > 2:
                data.append({
                    "symbol": "lock",
                    "value": symbol_info.value,
                    "trend": symbol_info.trend,
                    "swing": symbol_info.swing,
                    "dividend": symbol_info.dividend,
                    "chip": symbol_info.chip,
                    "marketCap": decimal_to_float(symbol_info.market_cap),
                    "correlation": "lock"
                })
                continue

            data.append({
                "symbol": symbol_info.symbol,
                "value": symbol_info.value,
                "trend": symbol_info.trend,
                "swing": symbol_info.swing,
                "dividend": symbol_info.dividend,
                "chip": symbol_info.chip,
                "marketCap": decimal_to_float(symbol_info.market_cap),
                "correlation": decimal_to_float(s.correlation)
            })

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _related_symbol_cache_key(plan: str, symbol: str) -> str:
        return f"{plan}_{symbol}_related_symbol"

    def watchlist_symbol_oriented_score(self, symbols: List[str]) -> dict:
        symbol_list = self.get_symbol_info_by_symbol(symbols)

        data = {}
        for s in symbol_list:
            data[s.symbol] = {
                "dividend": s.dividend,
                "chip": s.chip,
                "swing": s.swing,
                "trend": s.trend,
                "value": s.value
            }

        return data

    def ai_sector_optional(self, oriented: str) -> dict:
        cache_key = self._ai_sector_optional_cache_key(oriented)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        am_avg_score = self._nike_sql_session.query(func.avg(getattr(SymbolInfo, oriented)).label("oriented")) \
            .filter(getattr(SymbolInfo, oriented) > 0) \
            .first()

        sector = []
        for s in SECTOR:
            sector_avg_score = self._nike_sql_session.query(func.avg(getattr(SymbolInfo, oriented)).label("oriented")) \
                .filter(getattr(SymbolInfo, oriented) > 0) \
                .filter(SymbolInfo.main_category == s) \
                .first()

            rank: List[SymbolInfo] = self._nike_sql_session.query(SymbolInfo) \
                .filter(getattr(SymbolInfo, oriented) > 0) \
                .filter(SymbolInfo.main_category == s) \
                .filter(SymbolInfo.volume_20MA > 3000000) \
                .filter(SymbolInfo.market_cap > 300000000) \
                .order_by(
                getattr(SymbolInfo, oriented).desc(), SymbolInfo.market_cap.desc(), SymbolInfo.volume_20MA.desc()) \
                .limit(5) \
                .all()

            tmp = []
            main_category_zh_tw = ""
            for r in rank:
                main_category_zh_tw = r.main_category_zh_tw
                tmp.append({
                    "symbol": r.symbol,
                    "score": getattr(r, oriented),
                    "marketCap": decimal_to_float(r.market_cap),
                    "companyName": r.name
                })
            sector.append({
                "mainCategory": s,
                "mainCategoryZhTw": main_category_zh_tw,
                "avgScore": decimal_to_float(sector_avg_score.oriented),
                "rank": tmp
            })
            sector = sorted(sector, key=lambda d: d["avgScore"], reverse=True)

        data = {
            "allMarketAvgScore": decimal_to_float(am_avg_score.oriented),
            "sector": sector
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _ai_sector_optional_cache_key(oriented: str) -> str:
        return f"{oriented}_ai_sector_optional"
