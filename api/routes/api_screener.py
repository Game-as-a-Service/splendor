from typing import List, Optional

from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.error import InvalidInvocation, DataValidationError
from api.biz.search_engine.screener_service import ScreenerService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_pagination_response
from api.containers.decorator import inject_service


class ApiScreener(Resource):

    @inject_service()
    def __init__(self, screener_service: ScreenerService) -> None:
        self._screener_service = screener_service

    @login_required()
    def get(self) -> Response:
        param = self.param_available()
        data, counts, page, page_size = self._screener_service.search(param)

        return api_pagination_response(data=data, message="Success", total=counts, page=page, page_size=page_size)

    def param_available(self) -> dict:
        param = {
            "value": self._check_list_fmt("value", request.args.getlist("value", type=int)),
            "trend": self._check_list_fmt("trend", request.args.getlist("trend", type=int)),
            "swing": self._check_list_fmt("swing", request.args.getlist("swing", type=int)),
            "chip": self._check_list_fmt("chip", request.args.getlist("chip", type=int)),
            "dividend": self._check_list_fmt("dividend", request.args.getlist("dividend", type=int)),
            "sector": self._check_list_fmt("sector", request.args.getlist("sector", type=str)),
            "industry": self._check_list_fmt("industry", request.args.getlist("industry", type=str)),
            "market_cap": self._check_int_fmt("marketCap", request.args.get("marketCap", type=int)),
            "volume_20MA": self._check_int_fmt("volume20MA", request.args.get("volume20MA", type=int)),
            "power_squeeze_daily": self._check_list_fmt("powerSqueezeDaily",
                                                        request.args.getlist("powerSqueezeDaily", type=int)),
            "power_squeeze_weekly": self._check_list_fmt("powerSqueezeWeekly",
                                                         request.args.getlist("powerSqueezeWeekly", type=int)),
            "surfing_trend_daily": self._check_int_fmt("surfingTrendDaily",
                                                       request.args.get("surfingTrendDaily", type=int)),
            "surfing_trend_weekly": self._check_int_fmt("surfingTrendWeekly",
                                                        request.args.get("surfingTrendWeekly", type=int)),
            "page": self._check_page(request.args.get("page", type=int)),
            "page_size": self._check_page_size(request.args.get("pageSize", type=int)),
            "sort_by": self._check_list_fmt("sortBy", request.args.getlist("sortBy", type=str))
        }

        return param

    @staticmethod
    def _check_list_fmt(key: str, value: List) -> Optional[List]:
        if not isinstance(value, list):
            raise DataValidationError(f"{key} 參數格式錯誤")

        return value

    @staticmethod
    def _check_int_fmt(key: str, value: int) -> Optional[int]:
        if value is None:
            return value

        if not isinstance(value, int):
            raise DataValidationError(f"{key} 參數格式錯誤")

        return value

    @staticmethod
    def _check_page(page: int):
        if not page:
            raise InvalidInvocation("page 不可為 0 or None")
        if not isinstance(page, int):
            raise DataValidationError("page 參數格式錯誤")
        return page

    @staticmethod
    def _check_page_size(page_size: int):
        if not page_size:
            raise InvalidInvocation("pageSize 不可為 None")
        if not isinstance(page_size, int):
            raise DataValidationError("pageSize 參數格式錯誤")
        return page_size
