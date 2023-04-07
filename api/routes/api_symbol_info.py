from flask_restful import Resource
from requests import Response

from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolInfo(Resource):

    @inject_service()
    def __init__(self, symbol_info_service: SymbolInfoService) -> None:
        self._symbol_info_service = symbol_info_service

    def get(self, symbol: str) -> Response:
        data = self._symbol_info_service.symbol_info(symbol)
        return api_response(data=data, message="Success")
