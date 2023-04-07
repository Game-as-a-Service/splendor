from typing import Optional

from flask import Response
from flask_restful import Resource

from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiOnlineSymbols(Resource):

    @inject_service()
    def __init__(self, symbol_info_service: SymbolInfoService):
        self._symbol_info_service = symbol_info_service

    def get(self, oriented: Optional[str] = None) -> Response:
        data = self._symbol_info_service.online_symbols(oriented)
        return api_response(data=data, message="Success")
