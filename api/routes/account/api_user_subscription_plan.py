from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.account.normal_account_service import NormalAccountService
from api.biz.error import DataValidationError, InvalidInvocation
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiUserSubscriptionPlan(Resource):
    @inject_service()
    def __init__(self, normal_account_service: NormalAccountService):
        self._normal_account_service = normal_account_service

    def post(self) -> Response:
        req = request.get_json()
        if "userId" not in req:
            raise DataValidationError("缺少 userId 參數.")

        if not req["userId"]:
            raise InvalidInvocation("userId 不能為空值.")

        data = self._normal_account_service.get_user_subscription_plan(req["userId"])
        return api_response(data=data, message="Success")
