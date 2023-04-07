from logging import Logger
from typing import Optional, List, Tuple

import humps
from sqlalchemy.orm import Session, Query

from api.biz.search_engine import SCREENER_SORT_COLUMN
from api.common.number_utils import decimal_to_float
from dbmodels.nike.symbol_info import SymbolInfo


class ScreenerService:
    def __init__(self, logger: Logger, nike_sql_session: Session) -> None:
        self._logger = logger
        self._nike_sql_session = nike_sql_session

    def query_screener(self, param: dict) -> Tuple[int, List[SymbolInfo]]:
        query: Query = self._nike_sql_session.query(SymbolInfo)

        query = self._query_orient("value", param["value"], query)
        query = self._query_orient("trend", param["trend"], query)
        query = self._query_orient("swing", param["swing"], query)
        query = self._query_orient("chip", param["chip"], query)
        query = self._query_orient("dividend", param["dividend"], query)

        query = self._query_main_category(param["sector"], query)
        query = self._query_sub_category(param["industry"], query)

        query = self._query_market_cap(param["market_cap"], query)
        query = self._query_volume_20ma(param["volume_20MA"], query)

        query = self._query_power_squeeze_daily(param["power_squeeze_daily"], query)
        query = self._query_power_squeeze_weekly(param["power_squeeze_weekly"], query)

        query = self._query_surfing_trend_daily(param["surfing_trend_daily"], query)
        query = self._query_surfing_trend_weekly(param["surfing_trend_weekly"], query)

        query = self._query_sort(param["sort_by"], query)

        counts = query.count()
        offset = (param["page"] - 1) * param["page_size"]

        return counts, query.offset(offset).limit(param["page_size"]).all()

    @staticmethod
    def _query_orient(orient: str, value: Optional[list], query: Query) -> Query:
        if orient == "value":
            if 0 in value:
                return query
            return query.filter(SymbolInfo.value.in_(value))
        if orient == "trend":
            if 0 in value:
                return query
            return query.filter(SymbolInfo.trend.in_(value))
        if orient == "swing":
            if 0 in value:
                return query
            return query.filter(SymbolInfo.swing.in_(value))
        if orient == "chip":
            if 0 in value:
                return query
            return query.filter(SymbolInfo.chip.in_(value))
        if orient == "dividend":  # noqa: R503
            if 0 in value:
                return query
            return query.filter(SymbolInfo.dividend.in_(value))

    @staticmethod
    def _query_main_category(category: Optional[list], query: Query) -> Query:
        if not category:
            return query
        return query.filter(SymbolInfo.main_category_id.in_(category))

    @staticmethod
    def _query_sub_category(category: Optional[list], query: Query) -> Query:
        if not category:
            return query
        return query.filter(SymbolInfo.sub_category_id.in_(category))

    @staticmethod
    def _query_market_cap(market_cap: Optional[int], query: Query) -> Query:
        if market_cap == 1:
            return query.filter(SymbolInfo.market_cap < 300000000)
        if market_cap == 2:
            return query.filter(SymbolInfo.market_cap.between(300000000, 1999999999))
        if market_cap == 3:
            return query.filter(SymbolInfo.market_cap.between(2000000000, 9999999999))
        if market_cap == 4:
            return query.filter(SymbolInfo.market_cap >= 10000000000)
        return query

    @staticmethod
    def _query_volume_20ma(volume_20ma: Optional[int], query: Query) -> Query:
        if volume_20ma == 1:
            return query.filter(SymbolInfo.volume_20MA < 50000)
        if volume_20ma == 2:
            return query.filter(SymbolInfo.volume_20MA.between(50000, 1000000))
        if volume_20ma == 3:
            return query.filter(SymbolInfo.volume_20MA.between(1000000, 5000000))
        if volume_20ma == 4:
            return query.filter(SymbolInfo.volume_20MA.between(5000000, 10000000))
        if volume_20ma == 5:
            return query.filter(SymbolInfo.volume_20MA.between(10000000, 50000000))
        if volume_20ma == 6:
            return query.filter(SymbolInfo.volume_20MA >= 1000000)
        if volume_20ma == 7:
            return query.filter(SymbolInfo.volume_20MA >= 5000000)
        if volume_20ma == 8:
            return query.filter(SymbolInfo.volume_20MA >= 10000000)
        if volume_20ma == 9:
            return query.filter(SymbolInfo.volume_20MA >= 50000000)
        return query

    @staticmethod
    def _query_power_squeeze_daily(power_squeeze: List, query: Query) -> Query:
        if not power_squeeze:
            return query
        return query.filter(SymbolInfo.power_squeeze_daily.in_(power_squeeze))

    @staticmethod
    def _query_power_squeeze_weekly(power_squeeze: List, query: Query) -> Query:
        if not power_squeeze:
            return query
        return query.filter(SymbolInfo.power_squeeze_weekly.in_(power_squeeze))

    @staticmethod
    def _query_surfing_trend_daily(surfing_trend: int, query: Query) -> Query:
        if surfing_trend == 1:
            return query.filter(SymbolInfo.surfing_trend_daily == 1)
        if surfing_trend == -1:
            return query.filter(SymbolInfo.surfing_trend_daily == -1)
        return query

    @staticmethod
    def _query_surfing_trend_weekly(surfing_trend: int, query: Query) -> Query:
        if surfing_trend == 1:
            return query.filter(SymbolInfo.surfing_trend_weekly == 1)
        if surfing_trend == -1:
            return query.filter(SymbolInfo.surfing_trend_weekly == -1)
        return query

    @staticmethod
    def _query_sort(sort: List[str], query: Query) -> Query:
        if not sort:
            return query
        for s in sort:
            if s[0:-1] not in SCREENER_SORT_COLUMN:
                continue
            if s[-1] == "0":
                if s == "volume20MA0":
                    query = query.order_by(SymbolInfo.volume_20MA.desc())
                else:
                    query = query.order_by(getattr(SymbolInfo, humps.decamelize(s[0:-1])).desc())
            if s[-1] == "1":
                if s == "volume20MA1":
                    query = query.order_by(SymbolInfo.volume_20MA.asc())
                else:
                    query = query.order_by(getattr(SymbolInfo, humps.decamelize(s[0:-1])).asc())

        return query

    def search(self, param: dict) -> Tuple[List[dict], int, int, int]:
        counts, symbol_info = self.query_screener(param)
        data = []
        for s in symbol_info:
            data.append({
                "symbol": s.symbol,
                "value": s.value,
                "trend": s.trend,
                "swing": s.swing,
                "chip": s.chip,
                "dividend": s.dividend,
                "marketCap": decimal_to_float(s.market_cap),
                "volume20MA": decimal_to_float(s.volume_20MA),
                "powerSqueezeDaily": decimal_to_float(s.power_squeeze_daily),
                "powerSqueezeWeekly": decimal_to_float(s.power_squeeze_weekly),
                "surfingTrendDaily": decimal_to_float(s.surfing_trend_daily),
                "surfingTrendWeekly": decimal_to_float(s.surfing_trend_weekly)
            })

        return data, counts, param["page"], param["page_size"]
