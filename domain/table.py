from typing import List
from .resource import Resource
from .card import DevelopmentCard
from .noble import Noble

class Table:
    def __init__(self) -> None:
        self.resource = Resource()
        self.deck1:List[DevelopmentCard] = []
        self.deck2:List[DevelopmentCard]  = []
        self.deck3:List[DevelopmentCard]  = []
        self.nobles :List[Noble] =[]
        self.level1 = {0: DevelopmentCard, 1: DevelopmentCard, 2: DevelopmentCard, 3: DevelopmentCard}
        self.level2 = {0: DevelopmentCard, 1: DevelopmentCard, 2: DevelopmentCard, 3: DevelopmentCard}
        self.level3 = {0: DevelopmentCard, 1: DevelopmentCard, 2: DevelopmentCard, 3: DevelopmentCard}
    
    def init(self,player:int)->None:
        pass

    def replenish_card(self,level:int)->None:
        pass
    