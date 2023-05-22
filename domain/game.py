import uuid

from enum import Enum
from .table import Table
from .player import Player
from .resource import Resource, Token
from typing import List


class Game:
    def __init__(self) -> None:
        self.id = str
        self.status = Status.progressing
        self.table = Table()
        self.players: List[Player] = []
        self.isLastRound: bool = False

    def start_game(self) -> None:
        pass

    def set_last_round(self) -> None:
        pass

    def end_game(self) -> None:
        pass

    def get_token(self, player: Player, res: Resource):
        # player.resource.appendToken(res.token)
        player.resource.token.extend(res.token)
        # self.table.resource.removeToken(res.token)
        for x in res.token:
            self.table.resource.token.remove(Token.__members__[x.name])
        player.resource = self.tokens_to_resource(player.resource.token)
        self.table.resource = self.tokens_to_resource(self.table.resource.token)

    def tokens_to_resource(self, tokens: list[Token]) -> Resource:
        ret = Resource()
        for token in tokens:
            ret.__setattr__(token.name, ret.__getattribute__(token.name) + 1)
        return ret


class Status(Enum):
    progressing = "progressing"
    lastRound = "lastRound"
    end = "end"
