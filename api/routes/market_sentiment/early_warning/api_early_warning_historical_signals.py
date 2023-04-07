from flask_restful import Resource
from requests import Response

from api.biz.market_sentiment.early_warning_service import EarlyWarningService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiEarlyWarningHistoricalSignals(Resource):

    @inject_service()
    def __init__(self, early_warning_service: EarlyWarningService) -> None:
        self._early_warning_service = early_warning_service

    def get(self) -> Response:
        data = self._early_warning_service.historical_signals()
        return api_response(data=data, message="Success")
