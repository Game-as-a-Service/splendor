from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from requests import Response

from api.biz.account.business_account_service import BusinessAccountService
from api.biz.error import DataValidationError
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiBusinessAccountLogin(Resource):
    @inject_service()
    def __init__(self, business_account_service: BusinessAccountService) -> None:
        self._business_account_service = business_account_service

    def post(self) -> Response:
        req = request.get_json()
        self._check_payload(req)

        data = self._business_account_service.get_user(req["username"], req["password"])
        if not data:
            return api_response(message={
                "return_code": -401,
                "return_msg": "username and password are not working!",
            })

        access_token = create_access_token(
            identity=req["username"],
            additional_claims={
                "user_id": req["username"],
                "account_type": "business",
                "email": None,
                "plan": "Basic Yearly"
            }
        )

        return api_response(return_data={"token": access_token}, message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")
        for r in ["username", "password"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")
            if not isinstance(r, str):
                raise DataValidationError(f"{r} 應為字串型態.")
