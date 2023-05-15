from .resource import Resource
from .developmentcard import Developmentcard
from .bonus import Bonus
from .token import Token

class Player:
    def __init__(self):
        self.score:int=0
        self.resource:Resource=Resource()
        self.card:list[Developmentcard]=[]
        self.bonus:Bonus=Bonus()
    
    def get_token(self,token:Token):
        self.resource.add_token(token)
    
    def get_bonus(self,card:Developmentcard):
        self.bonus.add_bonus(card)

    def buy_developmentcard(self,card:Developmentcard):
        self.score+=card.score
        self.card.append(card)
        self.resource.spend_token(card.cost)
        self.bonus.add_bonus(card)
        
        



    