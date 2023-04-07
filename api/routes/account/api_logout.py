from flask import session
from flask_restful import Resource
from requests import Response

from api.common.jwt_utils import login_required
from api.common.response_utils import api_response


class ApiLogout(Resource):
    def __init__(self) -> None:
        pass

    @login_required()
    def post(self) -> Response:
        session.clear()
        return api_response(message="Success")
