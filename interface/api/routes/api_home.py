from flask_restful import Resource
from requests import Response

from interface.api.common.response_utils import api_response


class ApiHome(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self) -> Response:
        return api_response(message="API is alive.")
