from .resource import Resource
from .token import Token
class Developmentcard:
    def __init__(self,id=int,level=int,cost=list[Token],score=int,bonus=Token)->None:
        self.id:int=id
        self.level:int=level
        self.cost:list[Token]=cost
        self.score:int=score
        self.bonus:Token=bonus
        