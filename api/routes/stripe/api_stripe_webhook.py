from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.stripe.stripe_webhook_service import StripeWebhookService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiStripeWebhook(Resource):
    @inject_service()
    def __init__(self, stripe_webhook_service: StripeWebhookService) -> None:
        self._stripe_webhook_service = stripe_webhook_service

    def post(self) -> Response:
        body = request.data
        signature = request.headers["STRIPE_SIGNATURE"]

        self._stripe_webhook_service.webhook(body, signature)
        return api_response(message="Success")
