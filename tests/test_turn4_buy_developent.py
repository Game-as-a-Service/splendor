from domain.bonus import Bonus
from domain.game import Game
from domain.player import Player
from tests.base_domain import BaseDomain
from domain.resource import Resource
from typing import List

class BuyDevelopent(BaseDomain):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    #given 玩家四 test_buydevelopment_usercase08
    #       1.初始Bonus(4,3,1,1,0)
    #       2.初始Token(400330)
    #       3.Table(032024)
    #       4.手上持有3.6
    #when 購買3.6號牌 
    #then 1.玩家獲得3.6號牌            GainCard
    #     2.玩家手上3.6保留卡不見       Disappear
    #     3.結果Bonus(4,4,1,1,0)       SelfBonus
    #     4.結果Token(100110)          SelfToken
    def test_buydevelopment_usercase08_gaincard(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #then 1.玩家獲得3.6號牌

        expected_card = buyCard
        expected_id_level = str(expected_card.id) + str(expected_card.level)
        self.assertIn(expected_id_level, [str(card.id) + str(card.level) for card in p4.development_cards])

    def test_buydevelopment_usercase08_disappear(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #then 1.玩家手上3.6保留卡不見

        expected_card = buyCard
        expected_id_level = str(expected_card.id) + str(expected_card.level)
        self.assertNotIn(expected_id_level, [str(card.id) + str(card.level) for card in p4.reserveDevelopmentCards])

    def test_buydevelopment_usercase08_selfbonus(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        #       4.Table(032024)
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #then 1.   Bonus(4,4,1,1,0)

        self.assertEqual(4, p4.bonus.diamond)
        self.assertEqual(4, p4.bonus.sapphire)
        self.assertEqual(1, p4.bonus.emerald)
        self.assertEqual(1, p4.bonus.ruby)
        self.assertEqual(0, p4.bonus.onyx)

    def test_buydevelopment_usercase08_selftoken(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        #       4.Table(032024)
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #then 1.   Token(100300)

        self.assertEqual(2, p4.resource.diamond)
        self.assertEqual(0, p4.resource.sapphire)
        self.assertEqual(0, p4.resource.emerald)
        self.assertEqual(3, p4.resource.ruby)
        self.assertEqual(0, p4.resource.onyx)
        self.assertEqual(0, p4.resource.gold)

    def test_buyDdevelopment_usercase08_tabletoken(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        #       4.Table(032024)
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        cost =Resource(2,0,0,0,3,0)
        p4.buyDevelopmentCard(cost,buyCard)
        g.table.resource.appendToken(cost.token)
        #then 1.   Table Token(232054)

        self.assertEqual(2, g.table.resource.diamond)
        self.assertEqual(3, g.table.resource.sapphire)
        self.assertEqual(2, g.table.resource.emerald)
        self.assertEqual(0, g.table.resource.ruby)
        self.assertEqual(5, g.table.resource.onyx)
        self.assertEqual(4, g.table.resource.gold)

    def test_buydevelopment_usercase08_setscore(self):        
        #given 玩家一 
        #       1.初始Bonus(4,3,1,1,0)
        #       2.初始Token(400330)
        #       3.手上持有3.6
        #       4.Table(032024)
        g=self.turn4_init()
        p4 =g.players[0]
        #when 購買保留卡3.6號牌
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #then 1.   Bonus(4,4,1,1,0)

        self.assertEqual(12, p4.score)

    def test_buydevelopment_usercase09_gainnoble(self):        
        #given 玩家四
        #       1.Bonus(44110)  
        g=self.turn4_init()
        p4 =g.players[0]
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #when 購買保留卡3.6號牌
        g.isGetNoble(p4)
        #then 1.   玩家獲得貴族卡4
        self.assertIn(4, [noble.id for noble in p4.nobles])
    
    def test_buydevelopment_usercase09_deckchange(self):        
        #given 玩家四
        #       1.Bonus(44110)  
        g=self.turn4_init()
        p4 =g.players[0]
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #when 購買保留卡3.6號牌
        g.isGetNoble(p4)
        #then 1.   玩家獲得貴族卡4
        self.assertNotIn(4, [noble.id for noble in g.table.nobles])

    def test_buydevelopment_usercase09_deckchange(self):        
        #given 玩家四
        #       1.Bonus(44110)  
        g=self.turn4_init()
        p4 =g.players[0]
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #when 獲得貴族卡4
        g.isGetNoble(p4)
        #then 1.   桌面失去貴族卡4
        self.assertNotIn(4, [noble.id for noble in g.table.nobles])
    
    def test_buydevelopment_usercase09_scorechange(self):        
        #given 玩家四
        #       1.Bonus(44110)  
        g=self.turn4_init()
        p4 =g.players[0]
        buyCard =p4.getReserveDevelopmentCard(3,6)
        p4.buyDevelopmentCard(Resource(2,0,0,0,3,0),buyCard)
        #when 獲得貴族卡4
        g.isGetNoble(p4)
        #then 1.   玩家15分
        self.assertEqual(15, p4.score)

    def test_buydevelopment_usercase10_islastround(self):
        #Given
        g =Game()
        p1 =Player()
        g.add_player(p1)
        p1.score =15
        #when game.is_last_round
        g.is_last_round()
        #then
        self.assertEqual(True,g.isLastRound)

    def test_buydevelopment_usercase12_whoswinner(self):
        #Given
        g =Game()
        p1 =Player()
        g.add_player(p1)
        p1.score =10
        p2 =Player()
        g.add_player(p2)
        p2.score =14
        p3 =Player()
        g.add_player(p3)
        p3.score =10
        p4 =Player()
        g.add_player(p4)
        p4.score =15
        #when game.is_last_round
        g.whos_Winner()
        #then
        self.assertEqual(p4,g.whosWinner)

    def turn4_init(self)->Game:
        g =Game()
        #level1 table


        #round25 已無貴族卡1
        g.table.nobles.pop(2)
        g.table.nobles.pop(0)
        g.table.resource =Resource(0,3,2,0,2,4)

        
        #p1 status
        p4 =Player()
        p4.resource =Resource(4,0,0,3,3,0)
        
        p4.reserveDevelopmentCards.append(super().getCards(3,6))
        super().playerGetdevelopment_cards(super().getManyCards(1,[4,8,14,15,18,19]),p4)
        super().playerGetdevelopment_cards(super().getManyCards(2,[7,12]),p4)
        super().playerGetdevelopment_cards(super().getManyCards(3,[3]),p4)
 
        #decouple
        p4.bonus = Bonus(4,3,1,1,0)
        g.add_player(p4)
        return g 