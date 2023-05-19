from pydoc import plain
from requests import Response
from domain.noble import Noble

from tests.base_flask_test_case import BaseFlaskTestCase
from domain.bonus import Bonus
from domain.player import Player
from domain.resource import Resource, Token
from domain.card import DevelopmentCard
from typing import List
from interface.repository.mySQL.game.nobe_repository import NobeRepository

from application.play_action import PlayAction

class TestApiHome(BaseFlaskTestCase):
    level1: List[DevelopmentCard]
    level2: List[DevelopmentCard]
    level3: List[DevelopmentCard]
    nobes: List[Noble]
    def setUp(self) -> None:    
        self.level1 = self._getLevel1()
        self.level2 = self._getLevel2()
        self.level3 = self._getLevel3()
        self.nobes = self._getNobes()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_200_when_api_is_alive(self):
        """API狀態正常，應該回應200"""
        with self.app.test_client() as client:
            res: Response = client.get("/")
            self.assertEqual(200, res.status_code)
            self.assertEqual("API is alive.", res.json["message"])
            
    def getCards(self,level:int,id:int)->DevelopmentCard:
        if level ==1:
            return list(filter(lambda c: c.id == id, self.level1))[0]
        elif level ==2:
            return list(filter(lambda c: c.id == id, self.level2))[0]
        else:
            return list(filter(lambda c: c.id == id, self.level3))[0]

    def getManyCards(self,level:int,id:List[int])-> List[DevelopmentCard]:
        cards = []
        if level ==1:
            for i in id:
                cards.append(list(filter(lambda c: c.id == i, self.level1))[0])
        elif level ==2:
            for i in id:
                cards.append(list(filter(lambda c: c.id == i, self.level2))[0])
        else:
            for i in id:
                cards.append(list(filter(lambda c: c.id == i, self.level3))[0])
        return cards

    def playerGetdevelopment_cards(self,cards:List[DevelopmentCard],player:Player):
        for card in cards:
            player.appendCard(card)



    def _getLevel1(self):        
        level: List[DevelopmentCard]= [
                    DevelopmentCard(1, 1, 0, Resource(1, 1, 1, 0, 1),  Bonus(ruby=1)),
                    DevelopmentCard(1, 2, 0, Resource(1, 1, 0, 1, 1),  Bonus(emerald=1)),
                    DevelopmentCard(1, 3, 0, Resource(0, 2, 0, 2, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 4, 0, Resource(1, 0, 1, 2, 1),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 5, 0, Resource(0, 0, 2, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 6, 0, Resource(0, 0, 0, 3, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 7, 0, Resource(2, 2, 0, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 8, 0, Resource(1, 0, 2, 2, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 9, 0, Resource(0, 0, 1, 3, 1),  Bonus(onyx=1)),
                    DevelopmentCard(1, 10, 0, Resource(0, 0, 0, 0, 4),  Bonus(emerald=1)),
                    DevelopmentCard(1, 11, 0, Resource(1, 1, 0, 1, 2),  Bonus(emerald=1)),
                    DevelopmentCard(1, 12, 0, Resource(2, 0, 1, 0, 2),  Bonus(ruby=1)),
                    DevelopmentCard(1, 13, 0, Resource(3, 0, 0, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 14, 0, Resource(1, 0, 0, 0, 2),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 15, 0, Resource(0, 2, 1, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 16, 0, Resource(0, 2, 0, 0, 2),  Bonus(diamond=1)),
                    DevelopmentCard(1, 17, 0, Resource(0, 2, 3, 1, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 18, 0, Resource(0, 3, 0, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(1, 19, 0, Resource(3, 1, 0, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 20, 0, Resource(0, 2, 2, 0, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 21, 0, Resource(1, 3, 1, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 22, 0, Resource(0, 0, 0, 2, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 23, 0, Resource(0, 1, 2, 1, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 24, 0, Resource(1, 2, 1, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 25, 0, Resource(0, 0, 3, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 26, 0, Resource(2, 1, 1, 0, 1),  Bonus(ruby=1)),
                    DevelopmentCard(1, 27, 0, Resource(0, 0, 2, 0, 2),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 28, 0, Resource(1, 0, 1, 1, 1),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 29, 1, Resource(0, 0, 0, 4, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(1, 30, 0, Resource(2, 0, 0, 2, 0),  Bonus(ruby=1)),
                    DevelopmentCard(1, 31, 0, Resource(1, 0, 0, 1, 3),  Bonus(ruby=1)),
                    DevelopmentCard(1, 32, 1, Resource(0, 0, 4, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(1, 33, 0, Resource(0, 1, 1, 1, 1),  Bonus(diamond=1)),
                    DevelopmentCard(1, 34, 1, Resource(0, 4, 0, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 35, 0, Resource(2, 0, 2, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 36, 0, Resource(1, 1, 1, 1, 0),  Bonus(onyx=1)),
                    DevelopmentCard(1, 37, 0, Resource(0, 0, 0, 0, 3),  Bonus(onyx=1)),
                    DevelopmentCard(1, 38, 0, Resource(2, 1, 0, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(1, 39, 0, Resource(0, 1, 0, 2, 2),  Bonus(emerald=1)),
                    DevelopmentCard(1, 40, 1, Resource(4, 0, 0, 0, 0),  Bonus(ruby=1)),
        ]
        return level
        
    def _getLevel2(self):
        level: List[DevelopmentCard]= [
                    DevelopmentCard(2, 1, 1, Resource(3, 2, 2, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 2, 3, Resource(0, 6, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 3, 1, Resource(0, 2, 2, 3, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 4, 2, Resource(0, 0, 0, 5, 3),  Bonus(diamond=1)),
                    DevelopmentCard(2, 5, 2, Resource(0, 5, 3, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 6, 1, Resource(0, 0, 3, 2, 2),  Bonus(diamond=1)),
                    DevelopmentCard(2, 7, 1, Resource(2, 3, 0, 3, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 8, 2, Resource(0, 5, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 9, 2, Resource(0, 0, 0, 5, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 10, 2, Resource(0, 0, 5, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 11, 3, Resource(0, 0, 6, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 12, 3, Resource(6, 0, 0, 0, 0),  Bonus(diamond=1)),
                    DevelopmentCard(2, 13, 2, Resource(0, 0, 1, 4, 2),  Bonus(diamond=1)),
                    DevelopmentCard(2, 14, 3, Resource(0, 0, 0, 0, 6),  Bonus(onyx=1)),
                    DevelopmentCard(2, 15, 2, Resource(4, 2, 0, 0, 1),  Bonus(emerald=1)),
                    DevelopmentCard(2, 16, 3, Resource(0, 0, 0, 6, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 17, 2, Resource(5, 3, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 18, 1, Resource(2, 3, 0, 0, 2),  Bonus(emerald=1)),
                    DevelopmentCard(2, 19, 2, Resource(1, 4, 2, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 20, 1, Resource(2, 3, 0, 2, 0),  Bonus(ruby=1)),
                    DevelopmentCard(2, 21, 2, Resource(0, 0, 5, 3, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 22, 1, Resource(0, 3, 0, 2, 3),  Bonus(ruby=1)),
                    DevelopmentCard(2, 23, 1, Resource(0, 2, 3, 0, 3),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 24, 1, Resource(3, 0, 2, 3, 0),  Bonus(emerald=1)),
                    DevelopmentCard(2, 25, 1, Resource(3, 0, 3, 0, 2),  Bonus(onyx=1)),
                    DevelopmentCard(2, 26, 2, Resource(0, 0, 0, 0, 5),  Bonus(ruby=1)),
                    DevelopmentCard(2, 27, 2, Resource(3, 0, 0, 0, 5),  Bonus(ruby=1)),
                    DevelopmentCard(2, 28, 2, Resource(5, 0, 0, 0, 0),  Bonus(onyx=1)),
                    DevelopmentCard(2, 29, 2, Resource(2, 0, 0, 1, 4),  Bonus(sapphire=1)),
                    DevelopmentCard(2, 30, 0, Resource(2, 0, 0, 2, 0),  Bonus(ruby=1)),
        ]
        return level

    def _getLevel3(self):
        level: List[DevelopmentCard]= [
                    DevelopmentCard(3, 1, 5, Resource(0, 0, 0, 7, 3),  Bonus(onyx=1)),
                    DevelopmentCard(3, 2, 4, Resource(0, 0, 3, 6, 3),  Bonus(onyx=1)),
                    DevelopmentCard(3, 3, 4, Resource(3, 6, 3, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 4, 4, Resource(0, 0, 0, 0, 7),  Bonus(diamond=1)),
                    DevelopmentCard(3, 5, 5, Resource(0, 7, 3, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 6, 4, Resource(6, 3, 0, 0, 3),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 7, 3, Resource(5, 3, 0, 3, 3),  Bonus(emerald=1)),
                    DevelopmentCard(3, 8, 4, Resource(0, 0, 0, 7, 0),  Bonus(onyx=1)),
                    DevelopmentCard(3, 9, 4, Resource(0, 3, 6, 3, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 10, 3, Resource(3, 0, 3, 3, 5),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 11, 3, Resource(3, 5, 3, 0, 3),  Bonus(ruby=1)),
                    DevelopmentCard(3, 12, 3, Resource(0, 3, 3, 5, 3),  Bonus(diamond=1)),
                    DevelopmentCard(3, 13, 3, Resource(3, 3, 5, 3, 0),  Bonus(onyx=1)),
                    DevelopmentCard(3, 14, 4, Resource(0, 7, 0, 0, 0),  Bonus(emerald=1)),
                    DevelopmentCard(3, 15, 5, Resource(0, 0, 7, 3, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 16, 4, Resource(7, 0, 0, 0, 0),  Bonus(sapphire=1)),
                    DevelopmentCard(3, 17, 4, Resource(0, 0, 7, 0, 0),  Bonus(ruby=1)),
                    DevelopmentCard(3, 18, 5, Resource(3, 0, 0, 0, 7),  Bonus(diamond=1)),
                    DevelopmentCard(3, 19, 4, Resource(3, 0, 0, 3, 6),  Bonus(diamond=1)),
                    DevelopmentCard(3, 20, 5, Resource(7, 3, 0, 0, 0),  Bonus(sapphire=1)),
        ]
        return level
    
    def _getNobes(self):
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
        return nobles
    