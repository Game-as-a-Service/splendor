import validators
from flask import request, session
from flask_restful import Resource
from requests import Response

from api.biz.error import DataValidationError, InvalidInvocation
from api.biz.stripe.stripe_service import StripeService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiStripeCustomerPortal(Resource):

    @inject_service()
    def __init__(self, stripe_service: StripeService) -> None:
        self._stripe_service = stripe_service

    @login_required()
    def post(self) -> Response:
        user_id = session["user_id"]
        req = request.get_json()

        data = self._stripe_service.customer_portal(user_id, return_url=req["returnUrl"])
        return api_response(data=data, message="Success")

    @staticmethod
    def _check_payload(req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")

        for r in ["returnUrl"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")

        if not req["returnUrl"]:
            raise InvalidInvocation("returnUrl不能為空值.")

        if not validators.url(req["returnUrl"]):
            raise InvalidInvocation("returnUrl is not a valid url.")
