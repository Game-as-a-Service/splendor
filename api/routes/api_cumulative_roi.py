from flask_restful import Resource
from requests import Response

from api.biz.backtest.cumulative_roi_service import CumulativeRoiService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiCumulativeRoi(Resource):

    @inject_service()
    def __init__(self, cumulative_roi_service: CumulativeRoiService) -> None:
        self._cumulative_roi_service = cumulative_roi_service

    @login_required()
    def get(self, symbol: str, oriented: str, strategy: str, end_at: str) -> Response:
        data, message = self._cumulative_roi_service.get_cumulative_roi(symbol, oriented, strategy, end_at)
        return api_response(data=data, message=message)
