from flask import Response
from flask_restful import Resource

from api.biz.error import InvalidInvocation
from api.biz.video.video_info_service import VideoInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiVideoInfo(Resource):

    @inject_service()
    def __init__(self, video_info_service: VideoInfoService):
        self._video_info_service = video_info_service

    def get(self, category: str) -> Response:
        if category not in ["market-analysis", "oriented-analysis", "finance-knowledge"]:
            raise InvalidInvocation(f"category ({category}) is invalid.")

        data = self._video_info_service.video_info(category)
        return api_response(data=data, message="Success")
