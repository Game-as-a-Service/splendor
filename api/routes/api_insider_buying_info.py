from flask_restful import Resource
from requests import Response

from api.biz.error import InvalidInvocation
from api.biz.institution.insider_buying_info_service import InsiderBuyingInfoService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_pagination_response
from api.containers.decorator import inject_service


class ApiInsiderBuyingInfo(Resource):

    @inject_service()
    def __init__(self, insider_buying_info_service: InsiderBuyingInfoService) -> None:
        self._insider_buying_info_service = insider_buying_info_service

    @login_required()
    def get(self, symbol: str, page: str, page_size: str) -> Response:
        if int(page) == 0:
            raise InvalidInvocation("page 不能為 0.")

        data, total, updated_at = self._insider_buying_info_service.insider_buying_info(
            symbol, int(page), int(page_size))

        return api_pagination_response(
            data=data,
            page=int(page),
            page_size=int(page_size),
            total=total,
            updated_at=updated_at
        )
