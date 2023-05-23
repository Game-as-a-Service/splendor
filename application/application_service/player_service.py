
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

from interface.repository.mySQL.game import Repository
from ..user_case import *

class PlayerService:
    @inject_service()
    def __init__(self,
                 repository:Repository)->None:        
        self._player_repository =repository._player_repository
        self._development_card_repository =repository._development_card_repository
        self._table_repository = repository._table_repository

        #查
    def get_player_info(self,game_id:str,player_id:str)->dict:
        return self._player_repository.get_player_by_id(game_id,player_id).to_dict()   


    def buy_development_card_by_table(self,game_id:str,player_id:str,level:int,id:int,resource:ResourceUserCase)->None:
        #查
        player =self._player_repository.get_player_by_id(game_id,player_id).usercase_to_domain()
        cost =resource.usercase_to_domain()
        card =self._development_card_repository.get_development_card_info_by_id(level,id).usercase_to_domain()

        #改
        player.buyDevelopmentCard(cost,card)

        #存
        self._player_repository.set_player_by_id(game_id,player_id,player)
        

