from typing import List

from flask_caching import Cache

from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float


class HistoricalSymbolPriceService:
    def __init__(
            self,
            cache: Cache,
            symbol_service: SymbolService,
    ):
        self._cache = cache
        self._symbol_service = symbol_service

    def price(self, symbol: str, start_at: str, end_at: str) -> List[dict]:
        cache_key = self._price_cache_key(symbol, start_at, end_at)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        results = self._symbol_service.get_symbol_price(symbol, start_at, end_at)
        data = []
        for r in results:
            data.append({
                "date": date_to_str(r.time),
                "closePrice": decimal_to_float(r.adj_close_price)
            })
        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _price_cache_key(symbol: str, start_at: str, end_at: str) -> str:
        return f"{symbol}_price_{start_at}_{end_at}"
