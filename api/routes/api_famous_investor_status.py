from flask_restful import Resource
from requests import Response

from api.biz.institution.famous_investor_status_service import FamousInvestorStatusService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiFamousInvestorStatus(Resource):

    @inject_service()
    def __init__(self, famous_investor_status_service: FamousInvestorStatusService) -> None:
        self._famous_investor_status_service = famous_investor_status_service

    @login_required()
    def get(self, symbol: str) -> Response:
        data, four_quarters, updated_at = self._famous_investor_status_service.famous_investor_status(symbol)
        return api_response(data=data, fourQuarters=four_quarters, updatedAt=updated_at)
