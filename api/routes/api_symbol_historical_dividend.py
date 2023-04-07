from flask_restful import Resource
from requests import Response

from api.biz.historical.historical_dividend_service import HistoricalDividendService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolHistoricalDividend(Resource):

    @inject_service()
    def __init__(self, historical_dividend_service: HistoricalDividendService) -> None:
        self._historical_dividend_service = historical_dividend_service

    @login_required()
    def get(self, symbol: str, nums: str) -> Response:
        data = self._historical_dividend_service.dividend_info(symbol, int(nums))
        return api_response(data=data, message="Success")
