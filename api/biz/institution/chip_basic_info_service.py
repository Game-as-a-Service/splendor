from logging import Logger

from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.symbol.symbol_service import SymbolService
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.chip_basic_info import ChipBasicInfo


class ChipBasicInfoService:
    def __init__(
            self,
            cache: Cache,
            logger: Logger,
            nike_sql_session: Session,
            symbol_service: SymbolService,
            updated_at_utils: UpdatedAtUtils
    ):
        self._cache = cache
        self._logger = logger
        self._nike_sql_session = nike_sql_session
        self._symbol_service = symbol_service
        self._updated_at_utils = updated_at_utils

    def get_chip_basic_info_by_symbol(self, symbol: str) -> ChipBasicInfo:
        return self._nike_sql_session.query(ChipBasicInfo) \
            .filter(ChipBasicInfo.symbol == symbol) \
            .order_by(ChipBasicInfo.date.desc()) \
            .first()

    def chip_basic_info(self, symbol: str) -> dict:
        cache_key = self._chip_basic_info_cache_key(symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        chip_basic_info: ChipBasicInfo = self.get_chip_basic_info_by_symbol(symbol)
        if not chip_basic_info:
            return {
                "updatedAt": None,
                "cashSurplus": None,
                "cashNetIn": None,
                "cashNetOut": None,
                "addInstNum": None,
                "addTotalCash": None,
                "buildInstNum": None,
                "buildTotalCash": None,
                "reduceInstNum": None,
                "reduceTotalCash": None,
                "cleanInstNum": None,
                "cleanTotalCash": None
            }

        data = {
            "updatedAt": self._updated_at_utils.get_date("nike", "chip_basic_info"),
            "cashSurplus": chip_basic_info.cash_surplus,
            "cashNetIn": chip_basic_info.cash_net_in,
            "cashNetOut": chip_basic_info.cash_net_out,
            "addInstNum": chip_basic_info.add_inst_num,
            "addTotalCash": chip_basic_info.add_total_cash,
            "buildInstNum": chip_basic_info.build_inst_num,
            "buildTotalCash": chip_basic_info.build_total_cash,
            "reduceInstNum": chip_basic_info.reduce_inst_num,
            "reduceTotalCash": chip_basic_info.reduce_total_cash,
            "cleanInstNum": chip_basic_info.clean_inst_num,
            "cleanTotalCash": chip_basic_info.clean_total_cash
        }
        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _chip_basic_info_cache_key(symbol: str) -> str:
        return f"{symbol}_chip_basic_info"
