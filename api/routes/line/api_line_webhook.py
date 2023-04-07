from flask import request
from flask_restful import Resource

from api.biz.line.line_webhook_service import LineWebhookService
from api.containers.decorator import inject_service


class ApiLineWebhook(Resource):

    @inject_service()
    def __init__(self, line_webhook_service: LineWebhookService):
        self._line_webhook_service = line_webhook_service

    def post(self) -> str:
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)

        self._line_webhook_service.webhook(body, signature)

        return "OK"
