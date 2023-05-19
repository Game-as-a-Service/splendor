from typing import Optional

from flask import session
from sqlalchemy.orm import Session

from dbmodels.game_profile.game_info import GameInfo
from dbmodels.game_profile.player_info import PlayerInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation

from domain.game import Game
from domain.player import Player
from domain.resource import Resource


class GameRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session
        

    def get_game_by_id(self, id: str) -> Game:
        res =Game()
        game_info =self._user_sql_session.query(GameInfo).filter(GameInfo.game_id == id).first()
        res.id =id
        res.status = game_info.status
        player_info =self._user_sql_session.query(PlayerInfo).filter(PlayerInfo.game_id == id).all()
        for player in player_info:
            p =Player()
            p.id =player.player_id
            p.resource =Resource(player.diamond,player.sapphire,player.emerald,player.ruby,player.onyx,player.gold)
        return (
            self._user_sql_session.query(GameInfo)
            .filter(GameInfo.game_id == id)
            .first()
        )

