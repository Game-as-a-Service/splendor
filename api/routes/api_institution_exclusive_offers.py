from flask_restful import Resource
from requests import Response

from api.biz.account.institution_exclusive_offers_service import InstitutionExclusiveOffersService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiInstitutionExclusiveOffers(Resource):

    @inject_service()
    def __init__(self, institution_exclusive_offers_service: InstitutionExclusiveOffersService):
        self._institution_exclusive_offers_service = institution_exclusive_offers_service

    @login_required()
    def get(self, institution: str, collaborate: str) -> Response:
        data = self._institution_exclusive_offers_service.get_offer(institution, collaborate)
        return api_response(data=data, message="Success")
