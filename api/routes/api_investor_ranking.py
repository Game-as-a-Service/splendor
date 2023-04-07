from flask import request
from flask_restful import Resource
from requests import Response

from api.biz.error import InvalidInvocation
from api.biz.institution.investor_ranking_service import InvestorRankingService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_pagination_response
from api.containers.decorator import inject_service


class ApiInvestorRanking(Resource):

    @inject_service()
    def __init__(self, investor_ranking_service: InvestorRankingService) -> None:
        self._investor_ranking_service = investor_ranking_service

    @login_required()
    def get(self, symbol: str, page: int, page_size: int) -> Response:
        if page == 0:
            raise InvalidInvocation("page 不能為 0.")

        sort_by = request.args.getlist("sortBy", type=str)

        data, total, quarter, updated_at = self._investor_ranking_service.investor_ranking(
            symbol,
            page,
            page_size,
            sort_by
        )

        return api_pagination_response(
            data=data,
            page=page,
            page_size=page_size,
            total=total,
            quarter=quarter,
            updated_at=updated_at
        )
