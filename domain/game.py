
import uuid

from enum import Enum
from .table import Table
from .player import Player
from .resource import Resource,Token
from typing import List

class Game():
    def __init__(self) -> None:
        self.id =uuid.UUID("05d50d5d-4b64-4df7-bc40-334fffdf8102")
        self.status= Status.progressing
        self.table = Table()
        self.players:List[Player] = []
        self.isLastRound :bool =False
        self.whosWinner :Player

    def add_player(self, player:Player):
        self.players.append(player)
    def getToken(self, player:Player,res:Resource):
        player.resource.appendToken(res.token)
        self.table.resource.removeToken(res.token)    

    def is_last_round(self):
        if len(list(filter(lambda p:p.score>=15 ,self.players)))  >0:
            self.isLastRound =True

    def whos_Winner(self):
        self.whosWinner=max(self.players, key=lambda p: p.score)
        
    def isGetNoble(self,player:Player):
        pb = player.bonus
        for noble in self.table.nobles:
            nb =noble.bonus
            all_requirements_met = True
            gem_types = ['diamond', 'sapphire', 'emerald', 'ruby', 'onyx']
            for gem_type in gem_types:
                if getattr(pb, gem_type) < getattr(nb, gem_type):
                    all_requirements_met = False
                    break
            if all_requirements_met:
                self.table.nobles.remove(noble)
                player.nobles.append(noble)
                player.score+=noble.score
    def is_last_game(self):
        pass

class Status(Enum):
    progressing = "progressing"
    lastRound = "lastRound"
    end = "end"
