from datetime import date
from typing import List, Optional, Tuple

import humps
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session, Query

from api.biz.symbol.symbol_service import SymbolService
from dbmodels.nike.historical_market_indicator import HistoricalMarketIndicator
from dbmodels.nike.market_indicator_current_state import MarketIndicatorCurrentState
from dbmodels.nike.market_indicator_stats import MarketIndicatorStats
from dbmodels.nike.market_signal_list import MarketSignalList

SIGNAL_MAPPING = {
    "warning": -1,
    "beware": 0,
    "stable": 1
}


class MarketSentimentService:
    def __init__(self, nike_sql_session: Session, symbol_service: SymbolService) -> None:
        self._nike_sql_session = nike_sql_session
        self._symbol_service = symbol_service

    def get_data_latest_date(self, indicator: str) -> date:
        signal: HistoricalMarketIndicator = self._nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == indicator) \
            .order_by(HistoricalMarketIndicator.date.desc()) \
            .first()
        return signal.date

    def get_market_indicator_current(self, indicator: str) -> MarketIndicatorCurrentState:
        return self._nike_sql_session.query(MarketIndicatorCurrentState) \
            .filter(MarketIndicatorCurrentState.indicator == indicator) \
            .first()

    def get_historical_market_indicator(self, indicator: str, number: int = 0) -> List[HistoricalMarketIndicator]:
        """
        number: 抓取數量
        """
        if not number:
            return self._nike_sql_session.query(HistoricalMarketIndicator) \
                .filter(HistoricalMarketIndicator.indicator == indicator) \
                .order_by(HistoricalMarketIndicator.date.desc()) \
                .all()

        return self._nike_sql_session.query(HistoricalMarketIndicator) \
            .filter(HistoricalMarketIndicator.indicator == indicator) \
            .order_by(HistoricalMarketIndicator.date.desc()) \
            .limit(number) \
            .all()

    def get_market_indicator_stats(self, indicator: str, indicator_status: str) -> MarketIndicatorStats:
        return self._nike_sql_session.query(MarketIndicatorStats) \
            .filter(MarketIndicatorStats.indicator == indicator) \
            .filter(MarketIndicatorStats.indicator_status == indicator_status) \
            .first()

    def get_market_signal_list(
            self,
            indicator: str,
            signal: str,
            page: int,
            page_size: int,
            sort_by: Optional[str] = None
    ) -> Tuple[List[MarketSignalList], int]:
        query: Query = self._nike_sql_session.query(MarketSignalList) \
            .filter(MarketSignalList.indicator == indicator) \
            .filter(MarketSignalList.value == SIGNAL_MAPPING[signal])

        if not sort_by:
            query = query.order_by(MarketSignalList.start_at.desc())
        elif sort_by[-1] == "0":
            query = query.order_by(getattr(MarketSignalList, humps.decamelize(sort_by[0:-1])).desc())
        elif sort_by[-1] == "1":
            query = query.order_by(getattr(MarketSignalList, humps.decamelize(sort_by[0:-1])).asc())

        counts = query.count()

        offset = (page - 1) * page_size
        return query.offset(offset).limit(page_size).all(), counts

    def get_historical_market_indicator_to_dict(self, indicator: str) -> List[dict]:
        result: Result = self._nike_sql_session.execute(
            f"""SELECT * FROM historical_market_indicator WHERE `indicator`='{indicator}' ORDER BY `date` ASC;""")
        return result.mappings().all()
