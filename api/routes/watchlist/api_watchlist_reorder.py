from flask import session, request
from flask_restful import Resource
from requests import Response

from api.biz.error import DataValidationError, InvalidInvocation
from api.biz.watchlists import WatchlistServiceFacade
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiWatchlistReorder(Resource):
    @inject_service()
    def __init__(self, watchlist_service_facade: WatchlistServiceFacade) -> None:
        self._watchlist_service_facade = watchlist_service_facade

    @login_required()
    def post(self, watchlist_id) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])

        req = request.get_json()
        self._check_body(req)

        self._watchlist_service_facade.replace_symbols(
            session["account_type"], session["user_id"], watchlist_id, req["symbols"])

        return api_response(message="Success")

    @staticmethod
    def _check_body(req: dict) -> None:
        if "symbols" not in req:
            raise DataValidationError("缺少 symbols 參數.")

        if not isinstance(req["symbols"], list):
            raise InvalidInvocation("symbols 型態有誤.")
