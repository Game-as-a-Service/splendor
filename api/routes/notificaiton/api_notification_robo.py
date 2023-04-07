from typing import Optional

from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.notification.robo.robo_notification_service import RoboNotificationService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiNotificationRobo(Resource):

    @inject_service()
    def __init__(self, robo_notification_service: RoboNotificationService):
        self._robo_notification_service = robo_notification_service

    @login_required()
    def get(self, id: Optional[int] = None) -> Response:
        data = self._robo_notification_service.get_notification_robo(id)
        return api_response(data=data, message="Success")

    @login_required()
    def post(self) -> Response:
        payload = request.get_json()
        self._robo_notification_service.create_notification(payload)
        return api_response(message="Success")

    @login_required()
    def put(self, id: int) -> Response:
        payload = request.get_json()
        self._robo_notification_service.modify_notification_settings(id, payload)
        return api_response(message="Success")
