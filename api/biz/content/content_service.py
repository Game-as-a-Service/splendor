from logging import Logger

from sqlalchemy.orm import Session

from api.biz.symbol.symbol_service import SymbolService
from dbmodels.nike.description import Description


class ContentService:
    def __init__(self, logger: Logger, nike_sql_session: Session, symbol_info_service: SymbolService) -> None:
        self._logger = logger
        self._nike_sql_session = nike_sql_session
        self._symbol_info_service = symbol_info_service

    def get_content(self, symbol: str, oriented: str, info: str) -> Description:
        return self._nike_sql_session.query(Description) \
            .filter(Description.symbol == symbol) \
            .filter(Description.oriented == oriented) \
            .filter(Description.info == info) \
            .first()

    def content(self, symbol: str, oriented: str, info: str) -> dict:
        description: Description = self.get_content(symbol, oriented, info)

        if not description:
            return {"content": ""}
        return {"content": description.description}
