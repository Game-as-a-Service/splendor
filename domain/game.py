
import uuid

from enum import Enum
from .table import Table
from .player import Player
from typing import List
from .table import set_noble

class Game():
    def __init__(self) -> None:
        self.id =str
        self.status= Status.progressing
        self.table = Table()
        self.players:List[Player] = []
        self.isLastRound :bool =False

    
    def start_game(self)->None:
        self.table.set_gold()
        self.table.set_noble(len(self.players))

    def set_last_round(self)->None:
        pass

    def end_game(self)->None:
        pass

class Status(Enum):
    progressing = "progressing"
    lastRound = "lastRound"
    end = "end"
