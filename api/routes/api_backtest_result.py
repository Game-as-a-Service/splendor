from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.backtest.backtest_result_service import BacktestResultService
from api.biz.error import InvalidInvocation, TenantDataConflictError
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiBacktestResult(Resource):

    @inject_service()
    def __init__(self, backtest_result_service: BacktestResultService) -> None:
        self._backtest_result_service = backtest_result_service

    @login_required()
    def get(self, symbol: str, oriented: str, strategy: str) -> Response:
        if session["plan"] in ["Guest", "Free"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        if oriented not in ["value", "swing"]:
            raise InvalidInvocation("面向不在可請求範圍")

        data = self._backtest_result_service.backtest_result(symbol, oriented, strategy)
        return api_response(data=data, message="Success")
