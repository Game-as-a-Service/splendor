from flask_restful import Resource
from requests import Response

from api.biz.market_sentiment.fear_greed_service import FearGreedService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiFearAndGreedCurrent(Resource):

    @inject_service()
    def __init__(self, fear_greed_service: FearGreedService) -> None:
        self._fear_greed_service = fear_greed_service

    def get(self) -> Response:
        data = self._fear_greed_service.current()
        return api_response(data=data, message="Success")
