import json
from os import path

import validators
from flask import request, session
from flask_restful import Resource

from api.biz.error import DataValidationError, InvalidInvocation
from api.biz.stripe.stripe_webhook_service import StripeWebhookService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service

growin_stripe = (path.realpath(path.join(path.dirname(__file__), '..', 'static', 'growin-stripe.json')))


class ApiSubscribePlan(Resource):
    @inject_service()
    def __init__(self, stripe_webhook_service: StripeWebhookService) -> None:
        self._stripe_webhook_service = stripe_webhook_service
        self._growin_stripe = json.loads(open(growin_stripe, "r").read())

    @login_required()
    def post(self):
        user_id = session["user_id"]
        email = session["email"]
        req = request.get_json()
        self._check_payload(req)

        if req["discount"] in self._growin_stripe["expired"]:
            req["discount"] = None

        data = self._stripe_webhook_service.checkout_session_created(
            user_id=user_id,
            email=email,
            item=req["item"],
            success_url=req["successUrl"],
            cancel_url=req["cancelUrl"],
            discount=req["discount"]
        )
        return api_response(data=data, message="Success")

    def _check_payload(self, req: dict) -> None:
        if not isinstance(req, dict):
            raise DataValidationError("Body not json.")

        for r in ["item", "successUrl", "cancelUrl", "discount"]:
            if r not in req:
                raise DataValidationError(f"缺少 {r} 參數.")

        if req["item"] not in self._growin_stripe["item"]:
            raise InvalidInvocation("item is invalid.")

        if not req["successUrl"]:
            raise InvalidInvocation("successUrl must not be none.")

        if not req["cancelUrl"]:
            raise InvalidInvocation("cancelUrl must not be none.")

        if not validators.url(req["successUrl"]):
            raise InvalidInvocation("successUrl is not a valid url.")

        if not validators.url(req["cancelUrl"]):
            raise InvalidInvocation("cancelUrl is not a valid url.")

        if req["discount"] not in self._growin_stripe["discount"]:
            if req["discount"] in self._growin_stripe["expired"]:
                return
            raise InvalidInvocation("discount is invalid.")
