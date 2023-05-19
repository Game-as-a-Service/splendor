from importlib.resources import Resource
import uuid
from domain.game import Game
from domain.resource import Resource
from interface.repository.mySQL.game.nobe_repository import NobeRepository

from flask import request
from flask_restful import Resource
from requests import Response
from sqlalchemy import inspect

from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service

class PlayAction:
    @inject_service()
    def __init__(self,nobe_info_service:NobeRepository)->None:        
        self._nobe_info_service =nobe_info_service
        #查
    def query(self):
        data = self._nobe_info_service.get_nobe_info_by_nobe_id(1)
        print(data.diamond)

    def buyDevelopent(self,level:int,id:int,resource:Resource):
        buyCard =self.game.table.getCards(1,25)
        pass

