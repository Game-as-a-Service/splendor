from flask import session, request
from flask_restful import Resource, reqparse
from requests import Response

from api.biz.error import InvalidInvocation, TenantDataConflictError
from api.biz.notification.record import SORTED_BY, SORTED_WAY
from api.biz.notification.record.push_notification_record_service import PushNotificationRecordService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response, api_pagination_response
from api.containers.decorator import inject_service


class ApiNotificationRecord(Resource):

    @inject_service()
    def __init__(self, push_notification_record_service: PushNotificationRecordService):
        self._push_notification_record_service = push_notification_record_service

    @login_required()
    def get(self, page: int, page_size: int) -> Response:
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("sortBy", type=str, required=True, help='sortBy is required', location="args")
        args = parser.parse_args()

        self._check_parameter(args, page, page_size)

        user_id = session['user_id']
        account_type = session["account_type"]

        if account_type is None:
            raise TenantDataConflictError("guest 不能使用此功能.")

        total, data = self._push_notification_record_service.get_push_notification_record_by_token_user_id(
            user_id,
            page,
            page_size,
            args['sortBy']
        )

        return api_pagination_response(
            data=data,
            page=page,
            page_size=page_size,
            total=total
        )

    @login_required()
    def put(self, id: int | None = None) -> Response:
        payload = request.get_json()
        user_id = session['user_id']
        account_type = session["account_type"]

        if account_type is None:
            raise TenantDataConflictError("guest 不能使用此功能.")
        self._check_payload(payload)
        self._push_notification_record_service.update_push_notification_record_by_user_id(user_id, id, payload)

        return api_response(200, message="success")

    @staticmethod
    def _check_parameter(args, page, page_size) -> None:
        if page <= 0:
            raise InvalidInvocation("page 不能為 0.")

        if page_size <= 0:
            raise InvalidInvocation("page_size 不能為 0.")

        if args['sortBy'] not in [i + j for i in SORTED_BY for j in SORTED_WAY]:
            raise InvalidInvocation("sortBy 參數錯誤.")

    @staticmethod
    def _check_payload(payload) -> None:
        for key in ["readStatus"]:

            if key not in payload:
                raise InvalidInvocation(f"{key} is required.")

            if key == "readStatus":
                if payload['readStatus'] not in [0, 1]:
                    raise InvalidInvocation("readStatus 參數錯誤.")
