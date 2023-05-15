from domain.bonus import Bonus
from domain.game import Game
from domain.player import Player
from tests.base_domain import BaseDomain
from domain.resource import Resource, Token
from domain.card import DevelopmentCard
from typing import List

class GetToken(BaseDomain):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_gettoken_playerchange(self):
        #Given
        #       1.Table初始(052024)
        #       2.token初始(013001)
        g =Game()
        g.table.resource = Resource(0,5,2,0,2,4)
        p3 =Player()
        p3.resource =Resource(0,1,3,0,0,1)
        print(p3.resource.diamond)
        #when   拿2藍
        g.getToken(p3,Resource(0,2,0,0,0,0))
        print(p3.resource.diamond)
        #then   結果Token(033001)
        self.assertEqual(0, p3.resource.diamond)
        self.assertEqual(3, p3.resource.sapphire)
        self.assertEqual(3, p3.resource.emerald)
        self.assertEqual(0, p3.resource.ruby)
        self.assertEqual(0, p3.resource.onyx)
        self.assertEqual(1, p3.resource.gold)
    
    def test_gettoken_tablechange(self):
        #Given
        #       1.Table初始(052024)
        #       2.token初始(013001)
        g =Game()
        g.table.resource = Resource(0,5,2,0,2,4)
        p3 =Player()
        p3.resource =Resource(0,1,3,0,0,1)
        print(p3.resource.diamond)
        #when   拿2藍
        g.getToken(p3,Resource(0,2,0,0,0,0))
        print(p3.resource.diamond)
        #then   Table(032024)
        self.assertEqual(0, g.table.resource.diamond)
        self.assertEqual(3, g.table.resource.sapphire)
        self.assertEqual(2, g.table.resource.emerald)
        self.assertEqual(0, g.table.resource.ruby)
        self.assertEqual(2, g.table.resource.onyx)
        self.assertEqual(4, g.table.resource.gold)