from logging import Logger
from typing import List, Tuple, Optional

import humps
from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session, Query

from api.biz.institution import INVESTOR_RANKING_SORT_COLUMN
from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import datetime_to_quarter, str_to_date
from api.common.number_utils import decimal_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.sec13.sec_form_13f import SECForm13F


class InvestorRankingService:
    def __init__(
            self,
            cache: Cache,
            logger: Logger,
            sec13f_sql_session: Session,
            symbol_service: SymbolService,
            updated_at_utils: UpdatedAtUtils
    ) -> None:
        self._cache = cache
        self._logger = logger
        self._sec13f_sql_session = sec13f_sql_session
        self._symbol_service = symbol_service
        self._updated_at_utils = updated_at_utils

    def get_investor_ranking_calendar_date_by_symbol(self, symbol: str) -> SECForm13F:
        return self._sec13f_sql_session.query(SECForm13F) \
            .filter(SECForm13F.ticker == symbol) \
            .order_by(SECForm13F.calendardate.desc()) \
            .first()

    def get_investor_ranking_by_symbol(
            self,
            symbol: str,
            page: int,
            page_size: int,
            sort_by: Optional[List[str]],
            calendardate: Optional[str]
    ) -> Tuple[int, List[SECForm13F]]:

        query: Query = self._sec13f_sql_session.query(SECForm13F) \
            .filter(SECForm13F.ticker == symbol)

        if calendardate:
            query = query.filter(SECForm13F.calendardate == calendardate)

        count = query.count()

        if sort_by:
            for s in sort_by:
                if s[0:-1] not in INVESTOR_RANKING_SORT_COLUMN:
                    continue
                if s[-1] == "0":
                    query = query.order_by(getattr(SECForm13F, humps.decamelize(s[0:-1])).desc())
                if s[-1] == "1":
                    query = query.order_by(getattr(SECForm13F, humps.decamelize(s[0:-1])).asc())

        offset = (page - 1) * page_size

        return count, query.offset(offset).limit(page_size).all()

    def investor_ranking(
            self,
            symbol: str,
            page: int,
            page_size: int,
            sort_by: Optional[List[str]]
    ) -> Tuple[List[dict], int, str, str]:

        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        updated_at = self._updated_at_utils.get_date("13F", "SECForm13F")
        quarter = datetime_to_quarter(str_to_date(updated_at))

        total, results = self.get_investor_ranking_by_symbol(symbol, page, page_size, sort_by, updated_at)

        data = []
        for r in results:
            units_pct = decimal_to_float(r.units_pct)
            if units_pct is None and r.units != 0:
                units_pct = "建倉"

            if session["plan"] in ["Guest", "Free"]:
                data.append({
                    "investorname": r.investorname,
                    "style": r.style,
                    "units": "lock",
                    "unitsPct": "lock",
                    "value": "lock",
                    "weightPct": "lock"
                })
                continue

            data.append({
                "investorname": r.investorname,
                "style": r.style,
                "units": r.units,
                "unitsPct": units_pct,
                "value": r.value,
                "weightPct": decimal_to_float(r.weight_pct)
            })
        return data, total, quarter, updated_at
