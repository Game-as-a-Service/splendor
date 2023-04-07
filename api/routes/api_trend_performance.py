from flask_restful import Resource
from requests import Response

from api.biz.backtest.backtest_trend_service import BacktestTrendService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiTrendPerformance(Resource):

    @inject_service()
    def __init__(self, backtest_trend_service: BacktestTrendService) -> None:
        self._backtest_trend_service = backtest_trend_service

    @login_required()
    def get(self, symbol: str) -> Response:
        data = self._backtest_trend_service.trend_performance(symbol)
        return api_response(data=data, message="Success")
