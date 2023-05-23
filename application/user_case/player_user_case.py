from domain.player import Player
from .resource_user_case import ResourceUserCase
from .card_user_case import DevelopmentCardUserCase
from .bonus_user_case import BonusUserCase
from .noble_user_case import NobleUserCase


class PlayerUserCase:
    def __init__(self, score:int= None,
                         resource:ResourceUserCase= None,
                         development_cards:list[DevelopmentCardUserCase]= None,
                         reserve_cards:list[DevelopmentCardUserCase]= None,
                         bonus:BonusUserCase= None,
                         nobles:list[NobleUserCase]= None,
                         player:Player=None)->None:
        self.score=score
        self.resource =resource 
        self.development_cards=development_cards
        self.reserveDevelopmentCards=reserve_cards
        self.bonus=bonus
        self.nobles=nobles
        if player:
            self.domain_to_usercase(player)
    
    def domain_to_usercase(self,player:Player)->None:
        self.score= player.score
        self.resource = ResourceUserCase(player.resource)
        self.development_cards = [DevelopmentCardUserCase(card) for card in player.development_cards]
        self.reserveDevelopmentCards = [DevelopmentCardUserCase(card) for card in player.reserveDevelopmentCards]
        self.bonus = BonusUserCase(player.bonus)
        self.nobles = [NobleUserCase(noble) for noble in player.nobles]  

    def usercase_to_domain(self)->Player:
        p = Player()
        p.score =self.score
        p.resource =self.resource.usercase_to_domain()
        p.development_cards =[card.usercase_to_domain() for card in self.development_cards]
        p.reserveDevelopmentCards =[card.usercase_to_domain() for card in self.reserveDevelopmentCards]
        p.bonus = self.bonus.usercase_to_domain()
        p.nobles = [noble.user_to_domain() for noble in self.nobles] 
        return p

    @classmethod
    def to_usercase(cls,
                         score:int,
                         resource:ResourceUserCase,
                         development_cards:list[DevelopmentCardUserCase],
                         reserve_cards:list[DevelopmentCardUserCase],
                         bonus:BonusUserCase,
                         nobles:list[NobleUserCase])-> "PlayerUserCase":
        return cls(
            score = score,
            resource = resource,
            development_cards =development_cards,
            reserve_cards = reserve_cards,
            bonus = bonus,
            nobles= nobles)   
    
    def to_dict(self) -> dict:
        return {
            "score":self.score,
            "resource":self.resource.__dict__,
            "development_cards":[card.to_dict() for card in self.development_cards],
            "reserve_development_cards":[card.to_dict() for card in self.reserveDevelopmentCards],
            "bonus": self.bonus.__dict__,
            "nobles":[noble.to_dict() for noble in self.nobles],

        }