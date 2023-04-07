from flask_restful import Resource
from requests import Response

from api.biz.account.normal_account_service import NormalAccountService
from api.common.jwt_utils import login_required
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiLineAccountLinkStatus(Resource):
    @inject_service()
    def __init__(self, normal_account_service: NormalAccountService):
        self._normal_account_service = normal_account_service

    @login_required()
    def get(self) -> Response:
        data = self._normal_account_service.get_line_account_link_status()
        return api_response(data=data, message="Success")
