from flask_restful import Resource
from requests import Response

from api.biz.error import InvalidInvocation
from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiAiSectorOptional(Resource):

    @inject_service()
    def __init__(self, symbol_info_service: SymbolInfoService):
        self._symbol_info_service = symbol_info_service

    def get(self, oriented: str) -> Response:
        self._check_param(oriented)
        data = self._symbol_info_service.ai_sector_optional(oriented=oriented)
        return api_response(data=data, message="Success")

    @staticmethod
    def _check_param(oriented: str) -> None:
        if oriented not in ["value", "trend", "swing", "chip", "dividend"]:
            raise InvalidInvocation(f"{oriented} 不在可選擇的面向範圍。")
