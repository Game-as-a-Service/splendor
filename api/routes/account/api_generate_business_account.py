from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.account.business_account_service import BusinessAccountService
from api.biz.error import DataValidationError
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiGenerateBusinessAccount(Resource):
    @inject_service()
    def __init__(self, business_account_service: BusinessAccountService) -> None:
        self._business_account_service = business_account_service

    def post(self) -> Response:
        req = request.get_json()
        self._check_payload(req)

        self._business_account_service.generate_business_account(
            req["username"],
            req["password"],
            req["company"],
            req["companyCode"],
            req["plan"],
            req["subscribedAt"],
            req["expireAt"]
        )
        return api_response(message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")
        for r in ["username", "password", "company", "companyCode", "plan", "subscribedAt", "expireAt"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")
            if not isinstance(r, str):
                raise DataValidationError(f"{r} 應為字串型態.")
