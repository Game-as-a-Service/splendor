from flask_restful import Resource
from requests import Response

from api.biz.service_status.stock_mining_service import StockMiningServiceStatus
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiStockMiningServiceStatus(Resource):
    @inject_service()
    def __init__(self, stock_mining_service_status: StockMiningServiceStatus):
        self._stock_mining_service_status = stock_mining_service_status

    def get(self, service: str) -> Response:
        data = self._stock_mining_service_status.service(service)
        return api_response(data=data, message="Success")
