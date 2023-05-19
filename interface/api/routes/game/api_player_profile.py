from flask import request
from flask_restful import Resource
from requests import Response
from sqlalchemy import inspect
import json

from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service
from interface.repository.mySQL.account.user_info_service import UserInfoService

from application.application_service.player_service import PlayerService
from application.user_case import ResourceUserCase


class ApiPlayerProfile(Resource):
    @inject_service()
    def __init__(
        self,player_service:PlayerService
    ) -> None:
        self._player_service=player_service


    def get(self) -> Response:
        game_id = request.args.get("gameId")
        player_id = request.args.get("playerId")
        data = self._player_service.get_player_info(game_id,player_id).to_dict()    

        if not data:
            raise InvalidInvocation("user is not exists.")

        return api_response(data=data, message="Success")
    
class ApiPlayerBuyCardByTable(Resource):
    @inject_service()
    def __init__(
        self,player_service:PlayerService
    ) -> None:
        self._player_service=player_service

    def post(self) -> Response:
        data = request.json
        resource = ResourceUserCase(data['resource'])
        self._player_service.buy_development_card_by_table(data['game_id'],data['player_id'],data['level'],data['id'],resource)
        return api_response(message="Success")
        