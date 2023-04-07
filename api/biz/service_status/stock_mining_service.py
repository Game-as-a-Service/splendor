from sqlalchemy.orm import Session

from api.biz.error import InvalidInvocation
from api.common.datetime_utils import date_to_str
from dbmodels.nike.stock_mining_service import StockMiningService


class StockMiningServiceStatus:
    def __init__(self, nike_sql_session: Session):
        self._nike_sql_session = nike_sql_session

    def get_stock_mining_service(self, service: str) -> StockMiningService:
        return self._nike_sql_session.query(StockMiningService) \
            .filter(StockMiningService.service == service) \
            .first()

    def service(self, service: str) -> dict:
        stock_mining_service: StockMiningService = self.get_stock_mining_service(service)

        if not stock_mining_service:
            raise InvalidInvocation(f"個股探勘沒有 {service} 服務.")

        return {
            "activity": stock_mining_service.activity,
            "isFreeOpen": stock_mining_service.is_free_open,
            "openAt": date_to_str(stock_mining_service.open_at),
            "closeAt": date_to_str(stock_mining_service.close_at)
        }
