from datetime import date
from logging import Logger
from typing import Tuple, List

from flask import session
from flask_caching import Cache
from sqlalchemy.orm import Session, Query

from api.biz.symbol.symbol_service import SymbolService
from api.common.datetime_utils import date_to_str
from api.common.updated_at_utils import UpdatedAtUtils
from dbmodels.nike.insider_buying_info import InsiderBuyingInfo


class InsiderBuyingInfoService:
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

    def get_insider_buying_info_by_symbol(
            self,
            symbol: str,
            page: int,
            page_size: int
    ) -> Tuple[int, List[InsiderBuyingInfo]]:
        date_range = self.get_start_at_and_end_at()
        query: Query = self._nike_sql_session.query(InsiderBuyingInfo) \
            .filter(InsiderBuyingInfo.symbol == symbol) \
            .filter(InsiderBuyingInfo.filing_date.between(date_range["start_at"], date_range["end_at"]))

        if page == -1 and page_size == -1:
            return query.count(), query.order_by(InsiderBuyingInfo.filing_date.desc()).all()

        offset = (page - 1) * page_size
        return query.count(), query.order_by(InsiderBuyingInfo.filing_date.desc()).offset(offset).limit(page_size).all()

    def insider_buying_info(self, symbol: str, page: int, page_size: int) -> Tuple[List[dict], int, str]:
        symbol = self._symbol_service.symbol_mapping_by_symbol(symbol)
        updated_at = self._updated_at_utils.get_date("nike", "insider_buying_info")
        count, results = self.get_insider_buying_info_by_symbol(symbol, page, page_size)

        data = []
        for r in results:
            if session["plan"] in ["Guest", "Free"]:
                data.append({
                    "filingDate": date_to_str(r.filing_date),
                    "buyerName": r.buyer_name,
                    "buyerTitle": r.buyer_title,
                    "tradeDate": date_to_str(r.trade_date),
                    "tradeNum": "lock",
                    "tradeCash": "lock",
                    "tradeNumAfter": "lock",
                    "stockCategory": r.stock_category,
                    "stockCategoryZh": r.stock_category_zh
                })
                continue

            data.append({
                "filingDate": date_to_str(r.filing_date),
                "buyerName": r.buyer_name,
                "buyerTitle": r.buyer_title,
                "tradeDate": date_to_str(r.trade_date),
                "tradeNum": r.trade_num,
                "tradeCash": r.trade_cash,
                "tradeNumAfter": r.trade_num_after,
                "stockCategory": r.stock_category,
                "stockCategoryZh": r.stock_category_zh
            })

        return data, count, updated_at

    @staticmethod
    def get_start_at_and_end_at() -> dict:
        month = date.today().month
        year = date.today().year

        if month in [1, 2, 3]:
            return {
                "start_at": f"{year}-01-01 00:00:00",
                "end_at": f"{year}-03-31 00:00:00"
            }
        if month in [4, 5, 6]:
            return {
                "start_at": f"{year}-04-01 00:00:00",
                "end_at": f"{year}-06-30 00:00:00"
            }
        if month in [7, 8, 9]:
            return {
                "start_at": f"{year}-07-01 00:00:00",
                "end_at": f"{year}-09-30 00:00:00"
            }

        return {
            "start_at": f"{year}-10-01 00:00:00",
            "end_at": f"{year}-12-31 00:00:00"
        }
