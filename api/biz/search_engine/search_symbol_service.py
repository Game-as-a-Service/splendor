from typing import List

from sqlalchemy.orm import Session

from dbmodels.nike.symbol_info import SymbolInfo


class SearchSymbolService:
    def __init__(self, nike_sql_session: Session) -> None:
        self._nike_sql_session = nike_sql_session

    def search(self, keyword: str) -> List[dict]:
        stm = """
            SELECT symbol, name, country, main_category, main_category_zh_tw,
                CASE
                    WHEN symbol LIKE :keyword THEN 1
                    WHEN name LIKE :keyword  THEN 2
                END AS priority
            FROM symbol_info
            WHERE
                symbol LIKE :keyword OR name LIKE :keyword
            ORDER BY priority ASC;
        """
        results = self._nike_sql_session.execute(stm, {"keyword": f"{keyword}%"})

        data = []
        for r in results:
            data.append({
                "symbol": r.symbol,
                "name": r.name,
                "countryCode": r.country,
                "mainCategory": r.main_category,
                "mainCategoryZhTw": r.main_category_zh_tw
            })

        return data

    def default_search(self) -> List[dict]:
        symbol_list = ["AAPL", "TSLA", "NVDA", "AMZN", "TSM", "ABNB", "SBUX", "COST"]

        results: List[SymbolInfo] = self._nike_sql_session.query(SymbolInfo) \
            .filter(SymbolInfo.symbol.in_(symbol_list)) \
            .order_by(SymbolInfo.symbol) \
            .all()

        data = []
        for r in results:
            data.append({
                "symbol": r.symbol,
                "name": r.name,
                "countryCode": r.country,
                "mainCategory": r.main_category,
                "mainCategoryZhTw": r.main_category_zh_tw
            })

        return data
