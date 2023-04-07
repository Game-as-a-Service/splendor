import json
from os import path

from flask import Response
from flask_restful import Resource

from api.common.response_utils import api_response
from api.containers.decorator import inject_service

option = (path.realpath(path.join(path.dirname(__file__), '..', 'static', 'screener-option.json')))


class ApiScreenerOption(Resource):
    @inject_service()
    def __init__(self) -> None:
        pass

    def get(self) -> Response:
        data = json.loads(open(option, "r").read())
        return api_response(data=data, message="Success")
