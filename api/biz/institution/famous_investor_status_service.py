from logging import Logger
from typing import List, Tuple

from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session

from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import datetime_to_quarter, str_to_date
from api.common.number_utils import str_to_float
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.famous_investor_status import FamousInvestorStatus


class FamousInvestorStatusService:
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

    def get_famous_investor_status_by_symbol(self, symbol: str) -> List[FamousInvestorStatus]:
        return self._nike_sql_session.query(FamousInvestorStatus) \
            .filter(FamousInvestorStatus.symbol == symbol) \
            .all()

    def famous_investor_status(self, symbol: str) -> Tuple[List[List[dict]], List[str], str]:
        cache_key = self._famous_investor_status_cache_key(session["plan"], symbol)
        cached = self._cache.get(cache_key)
        if cached:
            return cached["data"], cached["fourQuarters"], cached["updatedAt"]

        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        updated_at = self._updated_at_utils.get_date("nike", "famous_investor_status")

        data = []
        four_quarters = []

        results: List[FamousInvestorStatus] = self.get_famous_investor_status_by_symbol(symbol)

        if results:
            four_quarters = [
                datetime_to_quarter(str_to_date(results[0].quarter_1)),
                datetime_to_quarter(str_to_date(results[0].quarter_2)),
                datetime_to_quarter(str_to_date(results[0].quarter_3)),
                datetime_to_quarter(str_to_date(results[0].quarter_4))
            ]

            for r in results:
                if session["plan"] in ["Guest", "Free"]:
                    data.append([
                        {"investorname": r.investorname, "investornameZh": r.investorname_zh},
                        {"units": "lock", "unitsPct": "lock"},
                        {"units": "lock", "unitsPct": "lock"},
                        {"units": str_to_float(r.units_3), "unitsPct": str_to_float(r.units_pct_3)},
                        {"units": str_to_float(r.units_4), "unitsPct": str_to_float(r.units_pct_4)},
                    ])
                    continue
                data.append([
                    {"investorname": r.investorname, "investornameZh": r.investorname_zh},
                    {"units": str_to_float(r.units_1), "unitsPct": str_to_float(r.units_pct_1)},
                    {"units": str_to_float(r.units_2), "unitsPct": str_to_float(r.units_pct_2)},
                    {"units": str_to_float(r.units_3), "unitsPct": str_to_float(r.units_pct_3)},
                    {"units": str_to_float(r.units_4), "unitsPct": str_to_float(r.units_pct_4)},
                ])

            self._cache.set(
                cache_key,
                {"data": data, "fourQuarters": four_quarters, "updatedAt": updated_at},
                timeout=3600
            )
        return data, four_quarters, updated_at

    @staticmethod
    def _famous_investor_status_cache_key(plan: str, symbol: str) -> str:
        return f"{plan}_{symbol}_famous_investor_status"
