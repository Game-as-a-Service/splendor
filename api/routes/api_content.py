from flask_restful import Resource

from api.biz.content.content_service import ContentService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiContent(Resource):

    @inject_service()
    def __init__(self, content_service: ContentService) -> None:
        self._content_service = content_service

    def get(self, symbol: str, oriented: str, info: str):
        data = self._content_service.content(symbol, oriented, info)
        return api_response(data=data, message="Success")
