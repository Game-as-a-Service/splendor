from flask import request, session
from flask_restful import Resource
from requests import Response

from api.biz.account.normal_account_service import NormalAccountService
from api.biz.error import InvalidInvocation, DataValidationError
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiUserProfile(Resource):
    @inject_service()
    def __init__(
            self,
            normal_account_service: NormalAccountService,

    ) -> None:

        self._normal_account_service = normal_account_service

    @login_required()
    def get(self) -> Response:

        data = self._normal_account_service.get_user(session["user_id"])

        if not data:
            raise InvalidInvocation("user is not exists.")

        data.update({"accountType": session["account_type"]})
        return api_response(data=data, message="Success")

    @staticmethod
    def _analyze_user() -> bool:
        if "x-api-key" not in request.headers:
            return False
        return True

    @staticmethod
    def _check_payload(payload: dict):
        if "watchlistIdx" not in payload:
            raise DataValidationError("watchlistIdx not in payload.")

        if not isinstance(payload["watchlistIdx"], int):
            raise DataValidationError("watchlistIdx type is invalid.")
