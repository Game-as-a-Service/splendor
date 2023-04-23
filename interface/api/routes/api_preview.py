from flask_restful import Resource

from interface.api.common.response_utils import api_response


class ApiPreview(Resource):
    def __init__(self):
        pass

    def get(self):
        return api_response(message="Success")
