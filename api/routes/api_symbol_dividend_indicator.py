from flask_restful import Resource
from requests import Response

from api.biz.indicator.dividend_indicator_service import DividendIndicatorService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolDividendIndicator(Resource):

    @inject_service()
    def __init__(self, dividend_indicator_service: DividendIndicatorService) -> None:
        self._dividend_indicator_service = dividend_indicator_service

    @login_required()
    def get(self, symbol: str) -> Response:
        data = self._dividend_indicator_service.dividend_indicator(symbol)
        return api_response(data=data, message="Success")
