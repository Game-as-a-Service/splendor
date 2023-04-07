from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.error import TenantDataConflictError
from api.biz.historical.historical_symbol_price_service import HistoricalSymbolPriceService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolPrice(Resource):
    @inject_service()
    def __init__(self, historical_symbol_price_service: HistoricalSymbolPriceService) -> None:
        self._historical_symbol_price_service = historical_symbol_price_service

    @login_required()
    def get(self, symbol: str, start_at: str, end_at: str) -> Response:
        if session["plan"] in ["Guest", "Free"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        data = self._historical_symbol_price_service.price(symbol, start_at, end_at)
        return api_response(data=data, message="Success")
