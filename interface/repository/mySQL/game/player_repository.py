from typing import Optional


from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import PlayerInfo,DevelopmentCardInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation


from application.user_case import PlayerUserCase,DevelopmentCardUserCase,NobleUserCase,BonusUserCase,ResourceUserCase
from .development_card_repository import DevelopmentCardRepository
from .nobe_repository import NobeRepository
from typing import List

import json


class PlayerRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session
        
        

    def get_player_by_id(self, game_id: str, player_id: str) -> PlayerUserCase:
        player_info =self.get_player_info_by_id(game_id,player_id)

        return PlayerUserCase.to_usercase(
            player_info.score,
            ResourceUserCase.to_usercase(player_info.diamond,player_info.sapphire,player_info.emerald,player_info.ruby,player_info.onyx,player_info.gold),
            DevelopmentCardRepository.get_player_development_card_info_by_id(self,game_id,player_id,True),
            DevelopmentCardRepository.get_player_development_card_info_by_id(self,game_id,player_id,False),
            BonusUserCase.to_usercase(player_info.bonus_diamond,player_info.bonus_sapphire,player_info.bonus_emerald,player_info.bonus_ruby,player_info.bonus_onyx),
            NobeRepository.get_player_node_info_by_id(self,game_id,player_id)
        )
    
    def set_player_by_id(self, game_id: str, player_id: str,player:PlayerUserCase) -> None:
        try:
            self._user_sql_session.begin()
            #player_info
            player_info = self._user_sql_session.query(PlayerInfo).filter(PlayerInfo.game_id == game_id, PlayerInfo.player_id == player_id).first()
            self._user_sql_session.merge(PlayerInfo.update(player_info,player))
            #delevepment 
            DevelopmentCardRepository.set_player_development_card_info_by_id(self,game_id,player_id,player.reserveDevelopmentCards,False)
            DevelopmentCardRepository.set_player_development_card_info_by_id(self,game_id,player_id,player.development_cards,True)

            
            self._user_sql_session.commit()
        except:
            self._user_sql_session.rollback()  
            raise
        finally:
            self._user_sql_session.close()  

    def get_player_info_by_id(self, game_id: str, player_id: str)->PlayerInfo:
        return(self._user_sql_session.query(PlayerInfo)
                      .filter(PlayerInfo.game_id == game_id,PlayerInfo.player_id == player_id)
                      .first())
    
    
    def get_card(self,level:int,id:int)->DevelopmentCardUserCase:
        return DevelopmentCardRepository.get_development_card_info_by_id(self,level,id)