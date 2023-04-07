from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.error import TenantDataConflictError
from api.biz.historical.historical_rating_service import HistoricalRatingService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiHistoricalRating(Resource):

    @inject_service()
    def __init__(self, historical_rating_service: HistoricalRatingService) -> None:
        self._historical_rating_service = historical_rating_service

    @login_required()
    def get(self, symbol: str, oriented: str) -> Response:
        if session["plan"] in ["Guest", "Free"]:
            session.clear()
            raise TenantDataConflictError("該用戶權限不足.")

        data = self._historical_rating_service.historical_rating(symbol, oriented)
        return api_response(data=data, message="Success")
