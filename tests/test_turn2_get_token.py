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

    def test_getToken_playerchange(self):
        #Given
        #       1.Table初始(153124)
        #       2.token初始(110210)
        g =Game()
        g.table.resource = Resource(1,5,3,1,2,4)
        p2 =Player()
        p2.resource =Resource(1,1,0,2,1,0)
        #when   拿1白1綠1紅
        g.getToken(p2,Resource(1,0,1,1,0,0))
        #then   結果Token(211310)
        self.assertEqual(2, p2.resource.diamond)
        self.assertEqual(1, p2.resource.sapphire)
        self.assertEqual(1, p2.resource.emerald)
        self.assertEqual(3, p2.resource.ruby)
        self.assertEqual(1, p2.resource.onyx)
        self.assertEqual(0, p2.resource.gold)
    
    def test_getToken_tablechange(self):
        #Given
        #       1.Table初始(153124)
        #       2.token初始(110210)
        g =Game()
        g.table.resource = Resource(1,5,3,1,2,4)
        p2 =Player()
        p2.resource =Resource(1,1,0,2,1,0)
        #when   拿1白1綠1紅
        g.getToken(p2,Resource(1,0,1,1,0,0))
        #then   Table(052024)
        self.assertEqual(0, g.table.resource.diamond)
        self.assertEqual(5, g.table.resource.sapphire)
        self.assertEqual(2, g.table.resource.emerald)
        self.assertEqual(0, g.table.resource.ruby)
        self.assertEqual(2, g.table.resource.onyx)
        self.assertEqual(4, g.table.resource.gold)
