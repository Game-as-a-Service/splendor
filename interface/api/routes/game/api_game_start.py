from flask_restful import Resource
from requests import Response
from flask import request
from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from application.user_case.game_user_case import GameUserCase
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service


class ApiGameStart(Resource):
    @inject_service()
    def __init__(self,game_user_case:GameUserCase) -> None:
        self._game_user_case =game_user_case

    def post(self) -> Response:
        input_data = request.json
        output_data = self._game_user_case.start_game(input_data['user_id'])        
        if not input_data:
            raise InvalidInvocation("user is not exists.")

        return api_response(data=output_data, message="Success")
