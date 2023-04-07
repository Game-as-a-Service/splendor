from flask import request, session
from flask_restful import Resource
from requests import Response

from api.biz.error import DataValidationError
from api.biz.watchlists import WatchlistServiceFacade
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiWatchlist(Resource):

    @inject_service()
    def __init__(self, watchlist_service_facade: WatchlistServiceFacade) -> None:
        self._watchlist_service_facade = watchlist_service_facade

    @login_required()
    def post(self, watchlist_id: str = None) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])

        req = request.get_json()
        self._check_payload(req)

        watchlist_id = self._watchlist_service_facade.add_watchlist(
            session["account_type"], session["user_id"], req["name"])

        return api_response(data={"watchlistId": watchlist_id}, message="Success")

    @login_required()
    def put(self, watchlist_id: str) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])

        req = request.get_json()
        self._check_payload(req)

        self._watchlist_service_facade.rename_watchlist(
            session["account_type"], session["user_id"], watchlist_id, req["name"])

        return api_response(message="Success")

    @login_required()
    def delete(self, watchlist_id: str) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])
        self._watchlist_service_facade.delete_watchlist(session["account_type"], session["user_id"], watchlist_id)

        return api_response(message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")
        for r in ["name"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")
        if not isinstance(req["name"], str):
            raise DataValidationError("name 應為字串型態.")
