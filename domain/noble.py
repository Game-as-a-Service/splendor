from .token import Token
from .resource import Resource
class Noble:
    def __init__(self,id=int,score=int,cost=Resource)->None:
        self.id:int=id
        self.cost:Resource()=cost
        self.score:int=score