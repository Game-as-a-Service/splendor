from typing import List

import humps
from flask_caching import Cache

from api.biz.indicator.indicator_result_service import IndicatorResultService
from api.common.datetime_utils import date_to_str, datetime_to_week
from api.common.number_utils import decimal_to_float
from dbmodels.nike.indicator_result import IndicatorResult


class TrendIndicatorService:
    def __init__(
            self,
            cache: Cache,
            indicator_result_service: IndicatorResultService,
    ):
        self._cache = cache
        self._indicator_result_service = indicator_result_service

    def trend_indicator(self, symbol: str) -> dict:
        cache_key = self._trend_indicator_cache_key(symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        indicators = {
            "power_squeeze_daily": 60,
            "power_squeeze_mom_daily": 60,
            "surfing_trend_daily": 60,
            "power_squeeze_weekly": 52,
            "power_squeeze_mom_weekly": 52,
            "surfing_trend_weekly": 52,
        }
        data = {}
        for ind in indicators:
            results: List[IndicatorResult] = self._indicator_result_service.get_indicator_result(
                symbol=symbol, indicator=[ind], nums=indicators[ind], start_at=None, end_at=None)

            data["updatedAt"] = None
            if results:
                data["updatedAt"] = date_to_str(results[0].created_at)

            tmp = []
            for r in results:
                tmp.append({
                    "date": date_to_str(r.date),
                    "value": decimal_to_float(r.value),
                    "week": datetime_to_week(r.date)
                })
            tmp.reverse()
            data[humps.camelize(ind)] = tmp

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _trend_indicator_cache_key(symbol: str) -> str:
        return f"{symbol}_trend_indicator"
