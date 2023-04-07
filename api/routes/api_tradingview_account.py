from flask import request, session
from flask_restful import Resource
from requests import Response

from api.biz.account.tradingview_account_service import TradingviewAccountService
from api.biz.error import DataValidationError, TenantDataConflictError
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiTradingviewAccount(Resource):

    @inject_service()
    def __init__(self, tradingview_account_service: TradingviewAccountService) -> None:
        self._tradingview_account_service = tradingview_account_service

    @login_required()
    def post(self) -> Response:
        if session["plan"] in ["Guest", "Free"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        user_id = session["user_id"]
        req = request.get_json()
        self._check_payload(req)

        self._tradingview_account_service.account(user_id, req["tradingviewAccount"])
        return api_response(message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")

        for r in ["tradingviewAccount"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")
