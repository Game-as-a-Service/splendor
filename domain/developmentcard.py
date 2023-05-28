from .token import Token
from .resource import Resource
class Developmentcard:
    def __init__(self,level=int,id=int,cost=Resource,score=int,bonus=Token)->None:
        self.level:int=level
        self.id:int=id        
        self.cost:Resource()=cost
        self.score:int=score
        self.bonus:Token=bonus
        
    def getlevel1(self):
        card:list[Developmentcard]=[
            Developmentcard(1, 1,Resource(1,1,1,0,1),0,Token.ruby),
            Developmentcard(1, 2,Resource(1,1,0,1,1),0,Token.emerald),
            Developmentcard(1, 3,Resource(0,2,0,2,0),0,Token.emerald),
            Developmentcard(1, 4,Resource(1,0,1,2,1),0,Token.sapphire),
            Developmentcard(1, 5,Resource(0,0,2,1,0),0,Token.onyx),
            Developmentcard(1, 6,Resource(0,0,0,3,0),0,Token.emerald),
            Developmentcard(1, 7,Resource(2,2,0,1,0),0,Token.onyx),
            Developmentcard(1, 8,Resource(1,0,2,2,0),0,Token.sapphire),
            Developmentcard(1, 9,Resource(0,0,1,3,1),0,Token.onyx),
            Developmentcard(1,10,Resource(0,0,0,0,4),1,Token.emerald),
            Developmentcard(1,11,Resource(1,1,0,1,2),0,Token.emerald),
            Developmentcard(1,12,Resource(2,0,1,0,2),0,Token.ruby),
            Developmentcard(1,13,Resource(3,0,0,0,0),0,Token.ruby),
            Developmentcard(1,14,Resource(1,0,0,0,2),0,Token.sapphire),
            Developmentcard(1,15,Resource(0,2,1,0,0),0,Token.ruby),
            Developmentcard(1,16,Resource(0,2,0,0,2),0,Token.diamond),
            Developmentcard(1,17,Resource(0,2,3,1,0),0,Token.sapphire),
            Developmentcard(1,18,Resource(0,3,0,0,0),0,Token.diamond),
            Developmentcard(1,19,Resource(3,1,0,0,1),0,Token.diamond),
            Developmentcard(1,20,Resource(0,2,2,0,1),0,Token.diamond),
            Developmentcard(1,21,Resource(1,3,1,0,0),0,Token.emerald),
            Developmentcard(1,22,Resource(0,0,0,2,1),0,Token.diamond),
            Developmentcard(1,23,Resource(0,1,2,1,1),0,Token.diamond),
            Developmentcard(1,24,Resource(1,2,1,1,0),0,Token.onyx),
            Developmentcard(1,25,Resource(0,0,3,0,0),0,Token.onyx),
            Developmentcard(1,26,Resource(2,1,1,0,1),0,Token.ruby),
            Developmentcard(1,27,Resource(0,0,2,0,2),0,Token.sapphire),
            Developmentcard(1,28,Resource(1,0,1,1,1),0,Token.sapphire),
            Developmentcard(1,29,Resource(0,0,0,4,0),1,Token.sapphire),
            Developmentcard(1,30,Resource(2,0,0,2,0),0,Token.ruby),
            Developmentcard(1,31,Resource(1,0,0,1,3),0,Token.ruby),
            Developmentcard(1,32,Resource(0,0,4,0,0),1,Token.diamond),
            Developmentcard(1,33,Resource(0,1,1,1,1),0,Token.diamond),
            Developmentcard(1,34,Resource(0,4,0,0,0),1,Token.onyx),
            Developmentcard(1,35,Resource(2,0,2,0,0),0,Token.onyx),
            Developmentcard(1,36,Resource(1,1,1,1,0),0,Token.onyx),
            Developmentcard(1,37,Resource(0,0,0,0,3),0,Token.onyx),
            Developmentcard(1,38,Resource(2,1,0,0,0),0,Token.emerald),
            Developmentcard(1,39,Resource(0,1,0,2,2),0,Token.emerald),
            Developmentcard(1,40,Resource(4,0,0,0,0),1,Token.ruby)
        ]
        return card
    
    def getlevel2(self):
        card:list[Developmentcard]=[
            Developmentcard(2, 1,Resource(3,2,2,0,0),1,Token.onyx),
            Developmentcard(2, 2,Resource(0,6,0,0,0),3,Token.sapphire),
            Developmentcard(2, 3,Resource(0,2,2,3,0),1,Token.sapphire),
            Developmentcard(2, 4,Resource(0,0,0,5,3),2,Token.diamond),
            Developmentcard(2, 5,Resource(0,5,3,0,0),2,Token.emerald),
            Developmentcard(2, 6,Resource(0,0,3,2,2),1,Token.diamond),
            Developmentcard(2, 7,Resource(2,3,0,3,0),1,Token.diamond),
            Developmentcard(2, 8,Resource(0,5,0,0,0),2,Token.sapphire),
            Developmentcard(2, 9,Resource(0,0,0,5,0),2,Token.diamond),
            Developmentcard(2,10,Resource(0,0,5,0,0),2,Token.emerald),
            Developmentcard(2,11,Resource(0,0,6,0,0),3,Token.emerald),
            Developmentcard(2,12,Resource(6,0,0,0,0),3,Token.diamond),
            Developmentcard(2,13,Resource(0,0,1,4,2),2,Token.diamond),
            Developmentcard(2,14,Resource(0,0,0,0,6),3,Token.onyx),
            Developmentcard(2,15,Resource(4,2,0,0,1),2,Token.emerald),
            Developmentcard(2,16,Resource(0,0,0,6,0),3,Token.ruby),
            Developmentcard(2,17,Resource(5,3,0,0,0),2,Token.sapphire),
            Developmentcard(2,18,Resource(2,3,0,0,2),1,Token.emerald),
            Developmentcard(2,19,Resource(1,4,2,0,0),2,Token.ruby),
            Developmentcard(2,20,Resource(2,3,0,2,0),1,Token.ruby),
            Developmentcard(2,21,Resource(0,0,5,3,0),2,Token.onyx),
            Developmentcard(2,22,Resource(0,3,0,2,3),1,Token.ruby),
            Developmentcard(2,23,Resource(0,2,3,0,3),1,Token.sapphire),
            Developmentcard(2,24,Resource(3,0,2,3,0),1,Token.emerald),
            Developmentcard(2,25,Resource(3,0,3,0,2),1,Token.onyx),
            Developmentcard(2,26,Resource(0,0,0,0,5),2,Token.ruby),
            Developmentcard(2,27,Resource(3,0,0,0,5),2,Token.ruby),
            Developmentcard(2,28,Resource(5,0,0,0,0),2,Token.onyx),
            Developmentcard(2,29,Resource(2,0,0,1,4),2,Token.sapphire),
            Developmentcard(2,30,Resource(2,0,0,2,0),0,Token.ruby),
        ]
        return card
    
    def getlevel3(self):
        card:list[Developmentcard]=[
            Developmentcard(3, 1,Resource(0,0,0,7,3),5,Token.onyx),
            Developmentcard(3, 2,Resource(0,0,3,6,3),4,Token.onyx),
            Developmentcard(3, 3,Resource(3,6,3,0,0),4,Token.emerald),
            Developmentcard(3, 4,Resource(0,0,0,0,7),4,Token.diamond),
            Developmentcard(3, 5,Resource(0,7,3,0,0),5,Token.emerald),
            Developmentcard(3, 6,Resource(6,3,0,0,3),4,Token.sapphire),
            Developmentcard(3, 7,Resource(5,3,0,3,3),3,Token.emerald),
            Developmentcard(3, 8,Resource(0,0,0,7,0),4,Token.onyx),
            Developmentcard(3, 9,Resource(0,3,6,3,0),4,Token.ruby),
            Developmentcard(3,10,Resource(3,0,3,3,5),3,Token.sapphire),
            Developmentcard(3,11,Resource(3,5,3,0,3),3,Token.ruby),
            Developmentcard(3,12,Resource(0,3,3,5,3),3,Token.diamond),
            Developmentcard(3,13,Resource(3,3,5,3,0),3,Token.onyx),
            Developmentcard(3,14,Resource(0,7,0,0,0),4,Token.emerald),
            Developmentcard(3,15,Resource(0,0,7,3,0),5,Token.ruby),
            Developmentcard(3,16,Resource(7,0,0,0,0),4,Token.sapphire),
            Developmentcard(3,17,Resource(0,0,7,0,0),4,Token.ruby),
            Developmentcard(3,18,Resource(3,0,0,0,7),5,Token.diamond),
            Developmentcard(3,19,Resource(3,0,0,3,6),4,Token.diamond),
            Developmentcard(3,20,Resource(7,3,0,0,0),5,Token.sapphire),
        ]
        return card