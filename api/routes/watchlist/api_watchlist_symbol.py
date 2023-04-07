from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.watchlists import WatchlistServiceFacade
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiWatchlistSymbol(Resource):

    @inject_service()
    def __init__(self, watchlist_service_facade: WatchlistServiceFacade) -> None:
        self._watchlist_service_facade = watchlist_service_facade

    @login_required()
    def post(self, watchlist_id: str, symbol: str) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])
        self._watchlist_service_facade.add_symbol(session["account_type"], session["user_id"], watchlist_id, symbol)

        return api_response(message="Success")

    @login_required()
    def delete(self, watchlist_id: str, symbol: str) -> Response:
        self._watchlist_service_facade.valid_identity(session["plan"])
        self._watchlist_service_facade.remove_symbol(session["account_type"], session["user_id"], watchlist_id, symbol)

        return api_response(message="Success")
