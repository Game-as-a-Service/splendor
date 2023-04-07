from flask_restful import Resource

from api.biz.institution.chip_basic_info_service import ChipBasicInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiChipBasicInfo(Resource):

    @inject_service()
    def __init__(self, chip_basic_info_service: ChipBasicInfoService) -> None:
        self._chip_basic_info_service = chip_basic_info_service

    def get(self, symbol: str):
        data = self._chip_basic_info_service.chip_basic_info(symbol)
        return api_response(data=data, message="Success")
