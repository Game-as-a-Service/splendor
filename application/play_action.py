from importlib.resources import Resource
import uuid
from domain.game import Game
from domain.resource import Resource

class PlayAction:
    def __init__(self,
            #game:uuid,player:uuid,
            game:Game):
        #查
        self.game =game

    def buyDevelopent(self,level:int,id:int,resource:Resource):
        buyCard =self.game.table.getCards(1,25)
        pass