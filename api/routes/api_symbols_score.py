from flask import request, session
from flask_restful import Resource
from requests import Response

from api.biz.error import DataValidationError, TenantDataConflictError
from api.biz.symbol.symbol_info_service import SymbolInfoService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiSymbolsScore(Resource):

    @inject_service()
    def __init__(self, symbol_info_service: SymbolInfoService) -> None:
        self._symbol_info_service = symbol_info_service

    @login_required()
    def post(self) -> Response:
        if session["plan"] in ["Guest"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        req = request.get_json()
        self._check_payload(req)

        data = self._symbol_info_service.watchlist_symbol_oriented_score(req["symbolList"])
        return api_response(data=data, message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")

        if "symbolList" not in req:
            raise DataValidationError("缺少 symbolList 參數")
