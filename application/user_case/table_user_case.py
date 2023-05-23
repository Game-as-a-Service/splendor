from domain import Table
from typing import List
from .resource_user_case import ResourceUserCase
from .card_user_case import DevelopmentCardUserCase
from .noble_user_case import NobleUserCase

class TableUserCase:
    def __init__(self,table:Table=None)->None:
        self.resource : ResourceUserCase
        self.deck1:List[DevelopmentCardUserCase]
        self.deck2:List[DevelopmentCardUserCase]
        self.deck3:List[DevelopmentCardUserCase]
        self.nobles :List[NobleUserCase]
        self.level1 : dict[int,DevelopmentCardUserCase] 
        self.level2 : dict[int,DevelopmentCardUserCase] 
        self.level3 : dict[int,DevelopmentCardUserCase] 
        if table:
            self.domain_to_usercase(table)
        
    def domain_to_usercase(self,table:Table)->None:
        self.resource = ResourceUserCase(table.resource)
        self.deck1:List[DevelopmentCardUserCase] = [DevelopmentCardUserCase(card) for card in table.deck1] 
        self.deck2:List[DevelopmentCardUserCase]  = [DevelopmentCardUserCase(card) for card in table.deck2] 
        self.deck3:List[DevelopmentCardUserCase]  = [DevelopmentCardUserCase(card) for card in table.deck3] 
        self.nobles :List[NobleUserCase] =[NobleUserCase(noble) for noble in table.nobles] 
        self.level1 : dict[int,DevelopmentCardUserCase] = {}
        for key, value in table.level1.items():
            self.level1[key] = DevelopmentCardUserCase(value)
        self.level2 : dict[int,DevelopmentCardUserCase] = {}
        for key, value in table.level2.items():
            self.level1[key] = DevelopmentCardUserCase(value)
        self.level3 : dict[int,DevelopmentCardUserCase] = {}
        for key, value in table.level3.items():
            self.level1[key] = DevelopmentCardUserCase(value)