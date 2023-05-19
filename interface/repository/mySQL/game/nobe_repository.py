from typing import Optional

from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import PlayerNobleInfo,NobleInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation
from domain import Noble,Bonus




class NobeRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session

    @staticmethod
    def get_player_node_info_by_id(self, game_id: str, player_id: str)->list[Noble]:
        noble_infos =(self._user_sql_session
                    .query(NobleInfo)
                    .join(PlayerNobleInfo, PlayerNobleInfo.noble_id == NobleInfo.noble_id)
                    .filter(PlayerNobleInfo.game_id == game_id)
                    .filter(PlayerNobleInfo.player_id == player_id)
                    .all())

        return [Noble(noble.noble_id, noble.score, Bonus(noble.diamond, noble.sapphire, noble.emerald, noble.ruby, noble.onyx)) for noble in noble_infos]

    @staticmethod
    def et_player_node_info_by_id(self, game_id: str, player_id: str,nobles:list[Noble])->None:
        nobles_origin =(self._user_sql_session
                    .query(PlayerNobleInfo)
                    .join(NobleInfo, PlayerNobleInfo.noble_id == NobleInfo.noble_id)
                    .filter(PlayerNobleInfo.game_id == game_id)
                    .filter(PlayerNobleInfo.player_id == player_id)
                    .all())
        
        nobles_new =[PlayerNobleInfo.from_noble(noble,game_id,player_id) for noble in nobles]
        for new in nobles_new:
            noble =list(filter(lambda c: c.id == new.id , nobles_origin))
            if noble==[]:
                self._user_sql_session.add(noble)              

