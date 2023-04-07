from typing import List, Tuple

from flask_caching import Cache
from stock_mining.stock_mining import Stock_mining

from config.api_config import Config


class CumulativeRoiService:
    def __init__(
            self,
            cache: Cache,
            config: Config
    ):
        self._cache = cache
        self._config = config
        self._stock_mining = Stock_mining(db_env=self._config.ENV_SET.upper())

    def get_cumulative_roi(self, symbol: str, oriented: str, strategy: str, end_at: str) -> Tuple[List[dict], str]:
        cache_key = self._cumulative_roi_cache_key(symbol, oriented, strategy, end_at)
        cached = self._cache.get(cache_key)
        if cached:
            return cached["data"], cached["message"]

        data = self._stock_mining.cum_ret_calculator(symbol, oriented, strategy, end_at)
        if data["message"] != "Success":
            return [], data["message"]

        self._cache.set(cache_key, data, timeout=3600)
        return data["data"], data["message"]

    @staticmethod
    def _cumulative_roi_cache_key(symbol: str, oriented: str, strategy: str, end_at: str) -> str:
        return f"{symbol}_{oriented}_{strategy}_{end_at}_cumulative_roi"
