from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.error import InvalidInvocation
from api.biz.market_sentiment.early_warning_service import EarlyWarningService
from api.common.response_utils import api_pagination_response
from api.containers.decorator import inject_service

SORT_BY = [
    "startAt0",
    "startAt1",
    "endAt0",
    "endAt1",
    "duration0",
    "duration1",
    "cumReturn0",
    "cumReturn1",
    "maxDrawdown0",
    "maxDrawdown1",
    "event0",
    "event1"
]


class ApiEarlyWarningHistoricalDetails(Resource):

    @inject_service()
    def __init__(self, early_warning_service: EarlyWarningService) -> None:
        self._early_warning_service = early_warning_service

    def get(self, signal: str, page: int, page_size: int) -> Response:
        sort_by = request.args.get("sortBy")
        self._check_params(signal, page, page_size, sort_by)

        data, total = self._early_warning_service.historical_details(signal, page, page_size, sort_by)
        return api_pagination_response(message="Success", data=data, page=page, page_size=page_size, total=total)

    @staticmethod
    def _check_params(signal: str, page: int, page_size: int, sort_by: str) -> None:
        if signal not in ["warning", "beware", "stable"]:
            raise InvalidInvocation(f"signal ({signal}) 不在可搜尋範圍")
        if page <= 0:
            raise InvalidInvocation("page 不能為 0.")
        if page_size <= 0:
            raise InvalidInvocation("page_size 不能為 0.")
        if sort_by and sort_by not in SORT_BY:
            raise InvalidInvocation(f"sortBy ({sort_by}) 不在可搜尋範圍")
