from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.notification.robo.robo_notification_service import RoboNotificationService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiNotificationRoboStatus(Resource):
    @inject_service()
    def __init__(self, robo_notification_service: RoboNotificationService):
        self._robo_notification_service = robo_notification_service

    @login_required()
    def post(self, id: int) -> Response:
        payload = request.get_json()
        self._robo_notification_service.modify_notification_status(id, payload)
        return api_response(message="Success")
