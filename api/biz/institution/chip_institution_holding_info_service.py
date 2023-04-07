from typing import List

from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import datetime_to_quarter
from api.common.number_utils import decimal_to_float
from dbmodels.nike.chip_institution_holding_info import ChipInstitutionHoldingInfo


class ChipInstitutionHoldingInfoService:
    def __init__(
            self,
            cache: Cache,
            nike_sql_session: Session,
            symbol_service: SymbolService
    ):
        self._cache = cache
        self._nike_sql_session = nike_sql_session
        self._symbol_service = symbol_service

    def get_chip_institution_holding_info_by_symbol(self, symbol: str) -> List[ChipInstitutionHoldingInfo]:
        return self._nike_sql_session.query(ChipInstitutionHoldingInfo) \
            .filter(ChipInstitutionHoldingInfo.symbol == symbol) \
            .order_by(ChipInstitutionHoldingInfo.date.desc()) \
            .limit(20) \
            .all()

    def chip_institution_holding_info(self, symbol: str) -> dict:
        cache_key = self._chip_institution_holding_info_cache_key(symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        results: List[ChipInstitutionHoldingInfo] = self.get_chip_institution_holding_info_by_symbol(symbol)

        info = []
        if not results:
            return {
                "headYear": None,
                "tailYear": None,
                "infos": info
            }

        for r in results:
            info.append({
                "date": datetime_to_quarter(r.date),
                "instOwnshp": decimal_to_float(r.inst_ownshp),
                "instCount": r.inst_count
            })

        data = {
            "headYear": int(info[-1]["date"][:4]),
            "tailYear": int(info[0]["date"][:4]),
            "infos": info
        }

        self._cache.set(cache_key, data, timeout=3600)
        return data

    @staticmethod
    def _chip_institution_holding_info_cache_key(symbol: str) -> str:
        return f"{symbol}_chip_institution_holding_info"
