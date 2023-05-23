from typing import List
from .resource import Resource, Token
from .card import DevelopmentCard
from .noble import Noble
from .bonus import Bonus
class Table:
    def __init__(self) -> None:
        self.resource = Resource()
        self.deck1:List[DevelopmentCard] = Table_init._getLevel1()
        self.deck2:List[DevelopmentCard]  = Table_init._getLevel2()
        self.deck3:List[DevelopmentCard]  = Table_init._getLevel3()
        self.nobles :List[Noble] =Table_init._getNobes(5)
        self.level1 : dict[int,DevelopmentCard] = {}
        self.level2 : dict[int,DevelopmentCard] = {}
        self.level3 : dict[int,DevelopmentCard] = {}

    
    def getCards(self, level: int, id: int) -> DevelopmentCard:
        if level == 1:
            key = next((key for key, card in self.level1.items() if card and card.id == id), None)
            if key is not None:
                return self.level1.pop(key)
        elif level == 2:
            key = next((key for key, card in self.level2.items() if card and card.id == id), None)
            if key is not None:
                return self.level2.pop(key)
        else:
            key = next((key for key, card in self.level3.items() if card and card.id == id), None)
        if key is not None:
            return self.level3.pop(key)
        
    def reissueCard(self):
        if len(self.level1)<=4:
            self.reissueCardByLevel(self.level1,self.deck1)
        if len(self.level2)<=4:
            self.reissueCardByLevel(self.level2,self.deck2)
        if len(self.level3)<=4:
            self.reissueCardByLevel(self.level3,self.deck3)

    def reissueCardByLevel(self, level:dict,deck:List[DevelopmentCard]):
        if 0 not in level:
            level[0] = deck.pop(0)
        if 1 not in level:
            level[1] = deck.pop(0)
        if 2 not in level:
            level[2] = deck.pop(0)
        if 3 not in level:
            level[3] = deck.pop(0)

#table初始化用 接DB後移除
class Table_init:
    def _getLevel1():        
        level: List[DevelopmentCard]= [
                    DevelopmentCard(1, 1, 0, Resource(0, 1, 1, 1, 1),  Bonus(ruby=1)),
                    DevelopmentCard(1, 2, 0, Resource(1, 1, 0, 1, 1),  Bonus(emerald=1)),
                    DevelopmentCard(1, 3, 0, Resource(2, 2, 0, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 4, 0, Resource(2, 0, 1, 1, 1),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 5, 0, Resource(1, 0, 2, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 6, 0, Resource(3, 0, 0, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 7, 0, Resource(1, 2, 0, 2, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 8, 0, Resource(2, 0, 2, 1, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 9, 0, Resource(3, 0, 1, 0, 1),  Bonus(onyx=1)),
                    DevelopmentCard(1, 10, 0, Resource(0, 0, 0, 0, 4),  Bonus(emerald=1)),
                    DevelopmentCard(1, 11, 0, Resource(1, 1, 0, 1, 2),  Bonus(emerald=1)),
                    DevelopmentCard(1, 12, 0, Resource(0, 0, 1, 2, 2),  Bonus(ruby=1)),
                    DevelopmentCard(1, 13, 0, Resource(0, 0, 0, 3, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 14, 0, Resource(0, 0, 0, 1, 2),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 15, 0, Resource(0, 2, 1, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 16, 0, Resource(0, 2, 0, 0, 2),  Bonus(diamond=1)),
                    DevelopmentCard(1, 17, 0, Resource(1, 2, 3, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 18, 0, Resource(0, 3, 0, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(1, 19, 0, Resource(0, 1, 0, 3, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 20, 0, Resource(0, 2, 2, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 21, 0, Resource(0, 3, 1, 1, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 22, 0, Resource(2, 0, 0, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 23, 0, Resource(1, 1, 2, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 24, 0, Resource(1, 2, 1, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 25, 0, Resource(0, 0, 3, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 26, 0, Resource(0, 1, 1, 2, 1),  Bonus(ruby=1)),
                    DevelopmentCard(1, 27, 0, Resource(0, 0, 2, 0, 2),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 28, 0, Resource(1, 0, 1, 1, 1),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 29, 1, Resource(4, 0, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 30, 0, Resource(2, 0, 0, 2, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 31, 0, Resource(1, 0, 0, 1, 3),  Bonus(ruby=1)),
                    DevelopmentCard(1, 32, 1, Resource(0, 0, 4, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(1, 33, 0, Resource(1, 1, 1, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 34, 1, Resource(0, 4, 0, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 35, 0, Resource(0, 0, 2, 2, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 36, 0, Resource(1, 1, 1, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 37, 0, Resource(0, 0, 0, 0, 3),  Bonus(onyx=1)),
                    DevelopmentCard(1, 38, 0, Resource(0, 1, 0, 2, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 39, 0, Resource(2, 1, 0, 0, 2),  Bonus(emerald=1)),
                    DevelopmentCard(1, 40, 1, Resource(0, 0, 0, 4, 0),  Bonus(ruby=1)),
        ]
        return level
        
    def _getLevel2():
        level: List[DevelopmentCard]= [
                    DevelopmentCard(2, 1, 1, Resource(0, 2, 2, 3, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 2, 3, Resource(0, 6, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 3, 1, Resource(3, 2, 2, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 4, 2, Resource(5, 0, 0, 0, 3),  Bonus(diamond=1)),
                    DevelopmentCard(2, 5, 2, Resource(0, 5, 3, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 6, 1, Resource(2, 0, 3, 0, 2),  Bonus(diamond=1)),
                    DevelopmentCard(2, 7, 1, Resource(3, 3, 0, 2, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 8, 2, Resource(0, 5, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 9, 2, Resource(5, 0, 0, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 10, 2, Resource(0, 0, 5, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 11, 3, Resource(0, 0, 6, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 12, 3, Resource(0, 0, 0, 6, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 13, 2, Resource(4, 0, 1, 0, 2),  Bonus(diamond=1)),
                    DevelopmentCard(2, 14, 3, Resource(0, 0, 0, 0, 6),  Bonus(onyx=1)),
                    DevelopmentCard(2, 15, 2, Resource(0, 2, 0, 4, 1),  Bonus(emerald=1)),
                    DevelopmentCard(2, 16, 3, Resource(6, 0, 0, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 17, 2, Resource(0, 3, 0, 5, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 18, 1, Resource(0, 3, 0, 2, 2),  Bonus(emerald=1)),
                    DevelopmentCard(2, 19, 2, Resource(0, 4, 2, 1, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 20, 1, Resource(2, 3, 0, 2, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 21, 2, Resource(3, 0, 5, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 22, 1, Resource(2, 3, 0, 0, 3),  Bonus(ruby=1)),
                    DevelopmentCard(2, 23, 1, Resource(0, 2, 3, 0, 3),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 24, 1, Resource(3, 0, 2, 3, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 25, 1, Resource(0, 0, 3, 3, 2),  Bonus(onyx=1)),
                    DevelopmentCard(2, 26, 2, Resource(0, 0, 0, 0, 5),  Bonus(ruby=1)),
                    DevelopmentCard(2, 27, 2, Resource(0, 0, 0, 3, 5),  Bonus(ruby=1)),
                    DevelopmentCard(2, 28, 2, Resource(0, 0, 0, 5, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 29, 2, Resource(1, 0, 0, 2, 4),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 30, 0, Resource(2, 0, 0, 2, 0),  Bonus(ruby=1)),
        ]
        return level

    def _getLevel3():
        level: List[DevelopmentCard]= [
                    DevelopmentCard(3, 1, 5, Resource(7, 0, 0, 0, 3),  Bonus(onyx=1)),
                    DevelopmentCard(3, 2, 4, Resource(6, 0, 3, 0, 3),  Bonus(onyx=1)),
                    DevelopmentCard(3, 3, 4, Resource(0, 6, 3, 3, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 4, 4, Resource(0, 0, 0, 0, 7),  Bonus(diamond=1)),
                    DevelopmentCard(3, 5, 5, Resource(0, 7, 3, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 6, 4, Resource(0, 3, 0, 6, 3),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 7, 3, Resource(3, 3, 0, 5, 3),  Bonus(emerald=1)),
                    DevelopmentCard(3, 8, 4, Resource(7, 0, 0, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(3, 9, 4, Resource(3, 3, 6, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 10, 3, Resource(3, 0, 3, 3, 5),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 11, 3, Resource(0, 5, 3, 3, 3),  Bonus(ruby=1)),
                    DevelopmentCard(3, 12, 3, Resource(5, 3, 3, 0, 3),  Bonus(diamond=1)),
                    DevelopmentCard(3, 13, 3, Resource(3, 3, 5, 3, 0),  Bonus(onyx=1)),
                    DevelopmentCard(3, 14, 4, Resource(0, 7, 0, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 15, 5, Resource(3, 0, 7, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 16, 4, Resource(0, 0, 0, 7, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 17, 4, Resource(0, 0, 7, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 18, 5, Resource(0, 0, 0, 3, 7),  Bonus(diamond=1)),
                    DevelopmentCard(3, 19, 4, Resource(3, 0, 0, 3, 6),  Bonus(diamond=1)),
                    DevelopmentCard(3, 20, 5, Resource(0, 3, 0, 7, 0),  Bonus(sapphire=1)),
        ]
        return level
    def _getNobes(number:int)->List[Noble]:
        nobles: List[Noble]= [
                    Noble(1, 3,Bonus(3,0,0,3,3)),
                    Noble(2, 3,Bonus(0,0,0,4,4)),
                    Noble(3, 3,Bonus(4,0,0,0,4)),
                    Noble(4, 3,Bonus(4,4,0,0,0)),
                    Noble(5, 3,Bonus(0,4,4,0,0)),
                    Noble(6, 3,Bonus(0,3,3,3,0)),
                    Noble(7, 3,Bonus(0,0,3,3,3)),
                    Noble(8, 3,Bonus(3,3,0,0,3)),
                    Noble(9, 3,Bonus(0,0,4,4,0)),
                    Noble(10,3,Bonus(3,3,3,0,0)),

        ]
        return nobles[:number]

