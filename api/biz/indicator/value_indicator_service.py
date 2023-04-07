from typing import List

import humps
from flask_caching import Cache

from api.biz.error import InvalidInvocation
from api.biz.indicator import VALUE_INDICATOR_MAP
from api.biz.indicator.indicator_result_service import IndicatorResultService
from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float
from dbmodels.nike.indicator_result import IndicatorResult


class ValueIndicatorService:
    def __init__(
            self,
            cache: Cache,
            symbol_service: SymbolService,
            indicator_result_service: IndicatorResultService
    ):
        self._cache = cache
        self._symbol_service = symbol_service
        self._indicator_result_service = indicator_result_service

    def value_indicator(self, symbol: str, indicator: str) -> dict:  # noqa: C901
        if indicator not in VALUE_INDICATOR_MAP:
            raise InvalidInvocation("indicator 不符合規定.")

        cache_key = self._value_indicator_cache_key(symbol, indicator)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)

        data = {}
        """
            PE-RATIO -> PE_stream_%d_%.1f (%d: 1~6, %.1f: 本益比倍數)
                        monthly_avg_price (月均價)
            Response Structure: {
                "PE_stream_1": {
                    "text": "%.1f本益比倍數",
                    "data": []
                },
                ···,
                "monthly_avg_price": []
            }
        """
        if indicator == "PE-RATIO":
            results: List[IndicatorResult] = \
                self._indicator_result_service.get_indicator_result(symbol, VALUE_INDICATOR_MAP[indicator])
            if not results:
                return data

            data["updatedAt"] = date_to_str(results[-1].created_at)

            for r in results:
                if r.indicator == "monthly_avg_price" and humps.camelize(r.indicator) not in data:
                    data[humps.camelize(r.indicator)] = [{
                        "date": date_to_str(r.date),
                        "score": decimal_to_float(r.value)
                    }]
                    continue

                if r.indicator == "monthly_avg_price" and humps.camelize(r.indicator) in data:
                    data[humps.camelize(r.indicator)].append({
                        "date": date_to_str(r.date),
                        "score": decimal_to_float(r.value)
                    })
                    continue

                if r.indicator[:11] in data:
                    data[r.indicator[:11]]["data"].append({
                        "date": date_to_str(r.date),
                        "score": decimal_to_float(r.value)
                    })
                    continue

                data[r.indicator[:11]] = {
                    "text": f"{r.indicator.split('_')[-1]}倍本益比",
                    "data": [{
                        "date": date_to_str(r.date),
                        "score": decimal_to_float(r.value)
                    }]
                }

            return data

        results: List[IndicatorResult] = \
            self._indicator_result_service.get_indicator_result(symbol, VALUE_INDICATOR_MAP[indicator])
        if not results:
            return data

        data["updatedAt"] = date_to_str(results[-1].created_at)
        for r in results:
            if r.indicator in data:
                data[r.indicator].append({
                    "date": date_to_str(r.date),
                    "score": decimal_to_float(r.value)
                })
                continue

            data[r.indicator] = [{
                "date": date_to_str(r.date),
                "score": decimal_to_float(r.value)
            }]

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _value_indicator_cache_key(symbol: str, indicator: str) -> str:
        return f"{symbol}_{indicator}_value_indicator"
