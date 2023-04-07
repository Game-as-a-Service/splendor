from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.account.normal_account_service import NormalAccountService
from api.biz.error import DataValidationError, InvalidInvocation
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiLineAccountLink(Resource):

    @inject_service()
    def __init__(self, normal_account_service: NormalAccountService):
        self._normal_account_service = normal_account_service

    @login_required()
    def post(self) -> Response:
        payload = request.get_json()
        self._normal_account_service.line_account_link(payload["nonce"])
        return api_response(message="Success")

    @staticmethod
    def _check_payload(payload: dict):
        if not isinstance(payload, dict):
            raise DataValidationError("payload 應該為 JSON 格式")

        if "nonce" not in payload:
            raise DataValidationError("缺少 nonce 參數")

        if not isinstance(payload["nonce"], str):
            raise InvalidInvocation("nonce 應該為字串格式")
