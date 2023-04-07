from flask_restful import Resource
from requests import Response

from api.biz.indicator.trend_indicator_service import TrendIndicatorService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolTrendIndicator(Resource):

    @inject_service()
    def __init__(
            self,
            trend_indicator_service: TrendIndicatorService
    ) -> None:
        self._trend_indicator_service = trend_indicator_service

    def get(self, symbol: str) -> Response:
        data = self._trend_indicator_service.trend_indicator(symbol)
        return api_response(data=data, message="Success")
