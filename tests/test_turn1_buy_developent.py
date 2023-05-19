from domain.bonus import Bonus
from domain.game import Game
from domain.player import Player
from tests.base_domain import BaseDomain
from domain.resource import Resource, Token
from domain.card import DevelopmentCard
from typing import List

class BuyDevelopent(BaseDomain):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    #given 玩家一 test_buy_development_usercase01
    #       1.初始Bonus(41233)
    #       2.初始Token(101110)
    #       3.table level1[20,21,25,24]
    #when 購買1.25號牌 
    #then 1.玩家獲得1.25號牌        GainCard
    #     2.桌面上1.25號牌已不存在   DeckChange
    #     3.結果Bonus(41233)        SelfBonus
    #     4.結果Token(100110)       SelfToken
    def test_buy_development_usercase01_gaincard(self):        
        #given 玩家一 
        #       1.初始Bonus(41233)
        #       2.初始Token(101110)
        #       3.table level1[20,21,25,24]
        g =self.turn1_init()
        #when 購買1.25號牌
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #then 1.玩家獲得1.25號牌
        #     2.桌面上1.25號牌已不存在
        #     3.結果Bonus(41233)
        #     4.結果Token(100110)
        
        #玩家獲得1.25號牌
        expected_card = buyCard
        expected_id_level = str(expected_card.id) + str(expected_card.level)
        self.assertIn(expected_id_level, [str(card.id) + str(card.level) for card in p1.development_cards])

    def test_buy_development_usercase01_deckchange(self):        
        #given 玩家一 
        #       1.初始Bonus(41233)
        #       2.初始Token(101110)
        #       3.table level1[20,21,25,24]
        g =self.turn1_init()
        #when 購買1.25號牌
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #then 1.玩家獲得1.25號牌
        #     2.桌面上1.25號牌已不存在
        #     3.結果Bonus(41233)
        #     4.結果Token(100110)
        
        #桌面上1.25號牌已不存在
        isExist = buyCard in g.table.level1.values()
        self.assertEqual(False,isExist)
       
    def test_buydevelopment_usercase01_selfbonus(self):
        #given 玩家一 
        #       1.初始Bonus(41233)
        #       2.初始Token(101110)
        #       3.table level1[20,21,25,24]
        g =self.turn1_init()
        #when 購買1.25號牌
         #when 購買1.25號牌
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #結果Bonus(41234)
        self.assertEqual(4, p1.bonus.diamond)
        self.assertEqual(1, p1.bonus.sapphire)
        self.assertEqual(2, p1.bonus.emerald)
        self.assertEqual(3, p1.bonus.ruby)
        self.assertEqual(4, p1.bonus.onyx)

    def test_buydevelopment_usercase01_selftoken(self):
        #given 玩家一 
        #       1.初始Bonus(41233)
        #       2.初始Token(101110)
        #       3.table level1[20,21,25,24]
        g =self.turn1_init()
        #when 購買1.25號牌
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #then 結果Token(100110)
        self.assertEqual(1, p1.resource.diamond)
        self.assertEqual(0, p1.resource.sapphire)
        self.assertEqual(0, p1.resource.emerald)
        self.assertEqual(1, p1.resource.ruby)
        self.assertEqual(1, p1.resource.onyx)
        self.assertEqual(0, p1.resource.gold)


    
    def test_buydevelopment_usercase02(self):
        #given 玩家一 
        #       玩家購買場面上卡片後
        g =self.turn1_init()
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #when:
        #       1.25號牌被購買,系統補牌        
        g.table.reissueCard()
        #then   1.3.table level1變成[20,21,26,24]
        self.assertEqual(26,g.table.level1[2].id)

    def test_buydevelopment_usercase03_gainnoble(self):
        #given 玩家一 
        #       Bonus被更新為(41234)
        g =self.turn1_init()
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #when:
        #       玩家回合結束game自動判斷Noble機制
        g.isGetNoble(p1)
        
        #then   玩家獲得貴族卡三
        self.assertIn(3, [noble.id for noble in p1.nobles])


    def test_buydevelopment_usercase03_tablecheck(self):
        #given 玩家一 
        #       Bonus被更新為(41234)
        g =self.turn1_init()
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        #when:
        #       玩家回合結束game自動判斷Noble機制
        g.isGetNoble(p1)
        #then   talbe貴族卡三被移除
        self.assertNotIn(3, [noble.id for noble in g.table.nobles])
    
    def test_buydevelopment_usercase04(self):
        #given 玩家一 
        #       Bonus被更新為(41234)
        g =self.turn1_init()
        p1 = g.players[0]
        buyCard =g.table.getCards(1,25)
        p1.buyDevelopmentCard(Resource(emerald=1),buyCard)
        
        #when:
        #       玩家回合結束game自動判斷Noble機制
        g.isGetNoble(p1)
        #then   talbe貴族卡三被移除
        self.assertEqual(10, p1.score)


    def turn1_init(self)->Game:
        g =Game()
        #level1 table
        g.table.level1[0] =super().getCards(1,20)
        g.table.level1[1] =super().getCards(1,21)
        g.table.level1[2] =super().getCards(1,25)
        g.table.level1[3] =super().getCards(1,24)
        
        

        #round25 已無貴族卡1
        g.table.nobles = g.table.nobles[1:]
        
        #level1 Deck
        g.table.deck1 =g.table.deck1[25:]

        #p1 status
        p1 = Player()
        p1.resource = Resource(1,0,1,1,1,0)
        super().playerGetdevelopment_cards(super().getManyCards(1,[1,5,7,9,10,11,12,13,17,22,23]),p1)
        super().playerGetdevelopment_cards(super().getManyCards(2,[6,9]),p1)
        super().playerGetNoble(super().getNoble(1),p1)
        #round25 7分
        p1.score =7
        #decouple
        p1.bonus = Bonus(4,1,2,3,3)
        g.add_player(p1)
        return g 