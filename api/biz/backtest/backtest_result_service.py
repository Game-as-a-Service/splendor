from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.error import DataNotFound
from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str
from api.common.number_utils import decimal_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.backtest_result import BacktestResult
from dbmodels.nike.symbol_info import SymbolInfo


class BacktestResultService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            symbol_info_service: SymbolInfoService,
            symbol_service: SymbolService,
            updated_at_utils: UpdatedAtUtils,
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._symbol_info_service = symbol_info_service
        self._symbol_service = symbol_service
        self._updated_at_utils = updated_at_utils

    def get_backtest_result(self, symbol: str, oriented: str, strategy: str) -> BacktestResult:
        return self._nike_sql_session.query(BacktestResult) \
            .filter(BacktestResult.symbol == symbol) \
            .filter(BacktestResult.oriented == oriented) \
            .filter(BacktestResult.strategy == strategy) \
            .order_by(BacktestResult.version.desc()) \
            .first()

    def backtest_result(self, symbol: str, oriented: str, strategy: str) -> dict:
        cache_key = self._backtest_result_cache_key(symbol, oriented, strategy)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol_info: SymbolInfo = self._symbol_info_service.get_symbol_info_by_symbol(symbol)
        if not symbol_info:
            raise DataNotFound(f"找不到指定的Symbol -> {symbol}")

        start_at, end_at = self._symbol_service.symbol_price_start_date_and_end_date(symbol_info.symbol)

        data = {
            "updatedAt": self._updated_at_utils.get_date("nike", "backtest_result"),
            "startAt": date_to_str(start_at, "%Y/%m"),
            "endAt": date_to_str(end_at, "%Y/%m"),
            "symbol": self._create_backtest_result(symbol, oriented, strategy),
            "sameIndustry": self._create_backtest_result(symbol_info.main_category, oriented, strategy),
            "allMarket": self._create_backtest_result("ALL_MARKET", oriented, strategy)
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _backtest_result_cache_key(symbol: str, oriented: str, strategy: str) -> str:
        return f"{symbol}_{oriented}_{strategy}_backtest_result"

    def _create_backtest_result(self, symbol: str, oriented: str, strategy: str) -> dict:
        backtest_result: BacktestResult = self.get_backtest_result(symbol, oriented, strategy)
        if not backtest_result or backtest_result.occurrence is None:
            return {
                "occurrence": None,
                "profits": None,
                "losses": None,
                "profitability": None,
                "avgHoldingTime": None,
                "avgProfitAndLoss": None,
                "avgProfit": None,
                "avgLoss": None,
                "avgProfitToLossRatio": None,
                "quantile25": None,
                "quantile50": None,
                "quantile75": None,
            }

        return {
            "occurrence": backtest_result.occurrence,
            "profits": backtest_result.profits,
            "losses": backtest_result.occurrence - backtest_result.profits,
            "profitability": decimal_to_float(backtest_result.profitability),
            "avgHoldingTime": decimal_to_float(backtest_result.avg_holding_time),
            "avgProfitAndLoss": decimal_to_float(backtest_result.avg_profit_and_loss),
            "avgProfit": decimal_to_float(backtest_result.avg_profit),
            "avgLoss": decimal_to_float(backtest_result.avg_loss),
            "avgProfitToLossRatio": decimal_to_float(backtest_result.avg_profit_to_loss_ratio),
            "quantile25": decimal_to_float(backtest_result.quantile_25),
            "quantile50": decimal_to_float(backtest_result.quantile_50),
            "quantile75": decimal_to_float(backtest_result.quantile_75),
        }
