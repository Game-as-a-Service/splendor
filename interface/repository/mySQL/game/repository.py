from typing import Optional

from flask import session
from sqlalchemy.orm import Session

from dbmodels.game_profile.game_info import GameInfo
from dbmodels.game_profile.player_info import PlayerInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation

from .development_card_repository import DevelopmentCardRepository
from .player_repository import PlayerRepository
from .table_repository import TableRepository


class Repository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session
        self._development_card_repository =DevelopmentCardRepository(self._user_sql_session)
        self._player_repository =PlayerRepository(self._user_sql_session)
        self._table_repository =TableRepository(self._user_sql_session)