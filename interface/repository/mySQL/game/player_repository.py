from typing import Optional

from flask import session
from sqlalchemy.orm import Session,joinedload

from dbmodels.game_profile import PlayerInfo
from interface.api.common.datetime_utils import date_to_str
from interface.api.common.error import InvalidInvocation


from application.user_case import PlayerUserCase
from .development_card_repository import DevelopmentCardRepository
from .nobe_repository import NobeRepository

import json


class PlayerRepository:
    def __init__(self, user_sql_session: Session) -> None:
        self._user_sql_session = user_sql_session
        
        

    def get_player_by_id(self, game_id: str, player_id: str) -> PlayerUserCase:
        player_info =self.get_player_info_by_id(game_id,player_id)
        return PlayerUserCase(
            player_info,
            DevelopmentCardRepository.get_player_development_card_info_by_id(self,game_id,player_id,True),
            DevelopmentCardRepository.get_player_development_card_info_by_id(self,game_id,player_id,False),
            NobeRepository.get_player_node_info_by_id(self,game_id,player_id)
        )
    
    def set_player_by_id(self, game_id: str, player_id: str,player:PlayerUserCase) -> None:
        try:
            self._user_sql_session.begin()
            #player_info
            player_info = self._user_sql_session.query(PlayerInfo).filter(PlayerInfo.game_id == game_id, PlayerInfo.player_id == player_id).first()
            player.player_user_case_to_player_info(player_info)
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
    
    