from flask_restful import Resource
from requests import Response

from api.biz.indicator.value_indicator_service import ValueIndicatorService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolValueIndicator(Resource):

    @inject_service()
    def __init__(self, value_indicator_service: ValueIndicatorService) -> None:
        self._value_indicator_service = value_indicator_service

    def get(self, symbol: str, indicator: str) -> Response:
        data = self._value_indicator_service.value_indicator(symbol, indicator)
        return api_response(data=data, message="Success")
