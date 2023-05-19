
import uuid
from domain.game import Game
from domain.resource import Resource

from flask import request
from flask_restful import Resource
from requests import Response
from sqlalchemy import inspect

from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service

from interface.repository.mySQL.game import PlayerRepository
from ..user_case import *

class PlayerService:
    @inject_service()
    def __init__(self,player_repository:PlayerRepository)->None:        
        self._player_repository =player_repository
        #查
    def get_player_info(self,game_id:str,player_id:str)->PlayerUserCase:
        return self._player_repository.get_player_by_id(game_id,player_id)    


    def buy_development_card_by_table(self,game_id:str,player_id:str,level:int,id:int,resource:ResourceUserCase):
        #查
        player =self._player_repository.get_player_by_id(game_id,player_id)
        #buyCard =self.game.table.getCards(1,25,resource)
        #改

        #存
        self._player_repository.set_player_by_id(game_id,player_id,player)
        pass

