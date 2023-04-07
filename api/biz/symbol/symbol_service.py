from datetime import datetime
from logging import Logger
from typing import List, Tuple

from flask_caching import Cache
from sqlalchemy.engine import CursorResult, Result
from sqlalchemy.orm import Session

from dbmodels.nike.symbol_mapping import SymbolMapping


class SymbolService:
    def __init__(self, cache: Cache, logger: Logger, nike_sql_session: Session, symbol_sql_session: Session) -> None:
        self._cache = cache
        self._logger = logger
        self._nike_sql_session = nike_sql_session
        self._symbol_sql_session = symbol_sql_session

    def symbol_mapping_by_symbol(self, symbol: str) -> str:
        symbol_mapping: SymbolMapping = self._nike_sql_session.query(SymbolMapping) \
            .filter(SymbolMapping.symbol == symbol) \
            .first()

        if not symbol_mapping:
            return symbol
        return symbol_mapping.target_symbol

    def symbol_price_start_date_and_end_date(self, symbol: str) -> Tuple[str, str]:
        sql = """
            SELECT
                MAX(time) AS end_at, MIN(time) AS start_at
            FROM
                history_bar
            WHERE
                symbol = :symbol;
        """
        results: CursorResult = self._symbol_sql_session.execute(sql, {"symbol": symbol})
        for r in results:
            start_at = max(r.start_at, datetime(2007, 1, 1))
            end_at = r.end_at
        return start_at, end_at

    def get_symbol_price(self, symbol: str, start_at: str, end_at: str) -> List[dict]:
        sql = """
            SELECT
                *
            FROM
                history_bar
            WHERE
                symbol = :symbol AND
                time BETWEEN STR_TO_DATE(:start_at, '%Y-%m-%d') AND STR_TO_DATE(:end_at, '%Y-%m-%d')
            ORDER BY
                time;
        """
        result: Result = self._symbol_sql_session.execute(
            sql,
            {"symbol": symbol, "start_at": start_at, "end_at": end_at}
        )
        return result.mappings().all()
