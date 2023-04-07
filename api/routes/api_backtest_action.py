from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.backtest.backtest_action_service import BacktestActionService
from api.biz.error import TenantDataConflictError
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiBacktestAction(Resource):

    @inject_service()
    def __init__(self, backtest_action_service: BacktestActionService) -> None:
        self._backtest_action_service = backtest_action_service

    @login_required()
    def get(self, symbol: str, oriented: str, strategy: str, start_at: str, end_at: str) -> Response:
        if session["plan"] in ["Guest", "Free"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        data = self._backtest_action_service.backtest_action(symbol, oriented, strategy, start_at, end_at)
        return api_response(data=data, message="Success")
