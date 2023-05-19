from domain.player import Player
from dbmodels.game_profile import PlayerInfo
from .resource_user_case import ResourceUserCase

class PlayerUserCase(Player):
    def __init__(self,player:PlayerInfo,development_cards,reserveDevelopmentCards,nobles):
        self.score :int=0
        self.resource= ResourceUserCase()
        self.development_cards= development_cards
        self.reserveDevelopmentCards= reserveDevelopmentCards
        self.nobles=nobles 
        self.bonus= super().setBonus()
        self.player_info_to_player_user_case(player)

    def player_info_to_player_user_case(self,player:PlayerInfo):
        self.score =player.score
        resource_attrs = ['diamond', 'sapphire', 'emerald', 'ruby', 'onyx','gold']
        for attr in resource_attrs:
            setattr(self.resource, attr, getattr(player, attr))
    
    def player_user_case_to_player_info(self,player_info:PlayerInfo)->None:
        player_info.score =self.score
        resource_attrs = ['diamond', 'sapphire', 'emerald', 'ruby', 'onyx','gold']
        for attr in resource_attrs:
            setattr(player_info, attr, getattr(self.resource, attr))

    def player_user_case_to_development_cards(self,player_info:PlayerInfo)->None:
        player_info.score =self.score
        resource_attrs = ['diamond', 'sapphire', 'emerald', 'ruby', 'onyx','gold']
        for attr in resource_attrs:
            setattr(player_info, attr, getattr(self.resource, attr))
