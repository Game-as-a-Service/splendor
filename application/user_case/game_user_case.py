from domain import Game
from .table_user_case import TableUserCase
from .player_user_case import PlayerUserCase
from typing import List
from enum import Enum

class GameUserCase:
    def __init__(self,game:Game=None)->None:
        self.id: str 
        self.status:StatusUserCase
        self.table:TableUserCase 
        self.players:List[PlayerUserCase]
        self.whosWinner :str
        if game:
            self.domain_to_usercase(game)

    def domain_to_usercase(self,game:Game)->None:
        self.id = game.id
        self.status = StatusUserCase(game.status.value)
        self.table = TableUserCase(game.table)
        self.players = [PlayerUserCase(player) for player in game.players] 
        self.whosWinner = game.whosWinner

class StatusUserCase(Enum):
    progressing = "progressing"
    lastRound = "lastRound"
    end = "end"
