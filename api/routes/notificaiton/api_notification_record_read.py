from flask import session
from flask_restful import Resource
from requests import Response

from api.biz.error import TenantDataConflictError
from api.biz.notification.record.push_notification_record_service import PushNotificationRecordService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiNotificationRecordRead(Resource):

    @inject_service()
    def __init__(self, push_notification_record_service: PushNotificationRecordService):
        self._push_notification_record_service = push_notification_record_service

    @login_required()
    def get(self) -> Response:
        user_id = session['user_id']
        account_type = session["account_type"]

        if account_type is None:
            raise TenantDataConflictError("guest 不能使用此功能.")

        res: bool = self._push_notification_record_service.is_exist_record_unread(user_id)

        return api_response(message='Success', data={'hasUnread': res})
