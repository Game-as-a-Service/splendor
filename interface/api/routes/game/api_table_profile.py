from flask import request
from flask_restful import Resource
from requests import Response
from sqlalchemy import inspect
import json

from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service

from application.application_service import G
from application.user_case import ResourceUserCase


class ApiTableProfile(Resource):
    @inject_service()
    def __init__(
        self,player_service:PlayerService
    ) -> None:
        self._player_service=player_service


    def get(self) -> Response:
        game_id = request.args.get("gameId")
        player_id = request.args.get("playerId")
        data = self._player_service.get_player_info(game_id,player_id)
        if not data:
            raise InvalidInvocation("user is not exists.")

        return api_response(data=data, message="Success")
    