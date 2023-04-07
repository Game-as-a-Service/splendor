from flask_restful import Resource

from api.biz.institution.chip_institution_holding_info_service import ChipInstitutionHoldingInfoService
from api.common.response_utils import api_response
from api.containers.decorator import inject_service


class ApiChipInstitutionHoldingInfo(Resource):

    @inject_service()
    def __init__(self, chip_institution_holding_info_service: ChipInstitutionHoldingInfoService) -> None:
        self._chip_institution_holding_info_service = chip_institution_holding_info_service

    def get(self, symbol: str):
        data = self._chip_institution_holding_info_service.chip_institution_holding_info(symbol)
        return api_response(data=data, message="Success")
