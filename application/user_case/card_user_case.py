from domain import DevelopmentCard,Token
from .resource_user_case import ResourceUserCase,TokenUserCase

class DevelopmentCardUserCase:
    def __init__(self,id:int=None,level:int=None,score:int=None,cost:ResourceUserCase=None,bonus:TokenUserCase=None,card:DevelopmentCard=None)->None:
        self.id =id
        self.level =level
        self.score =score
        self.cost =cost
        self.bonus=bonus
        if card:
            self.domain_to_usercase(card)

    def domain_to_usercase(self,card:DevelopmentCard)->None:
        self.id = card.id
        self.level = card.level
        self.score = card.score
        self.cost = card.cost
        self.bonus = TokenUserCase(card.bonus.value)
    
    def usercase_to_domain(self)->DevelopmentCard:
        return DevelopmentCard(self.id,self.level,self.score,self.cost.usercase_to_domain(),Token(self.bonus.value))
    
    @classmethod
    def to_usercase(cls,id:int,level:int,score:int,cost:ResourceUserCase,bonus:TokenUserCase)-> "DevelopmentCardUserCase":
        return cls(id,level,score,cost,bonus)   
    
    def to_dict(self)->dict:
        return {
            "id" :self.id,
            "level": self.level,
            "score": self.score,
            "cost": self.cost.to_dict_card(),
            "bonus": self.bonus.value
        }