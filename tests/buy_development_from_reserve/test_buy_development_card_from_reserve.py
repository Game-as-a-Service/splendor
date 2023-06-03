from domain.game import Game
from domain.player import Player

# from domain.table import Table
from domain.bonus import Bonus
from domain.resource import Resource, Token
from domain.card import DevelopmentCard


from tests.base_flask_test_case import BaseFlaskTestCase


class TestBuyDevelopmentCardFromReserve(BaseFlaskTestCase):
    """玩家擁有足夠的資源 -> 購買成功
    given:
        玩家Ａ
        沒有永久寶石
        有 1白1藍1紅1黑1黃金

        目前保留的發展卡為 lv1 No.11
    when:
        玩家Ａ購買手中保留的發展卡
    then:
        玩家Ａ
        獲得該發展卡
        保留中發展卡失去lv1 No.11
        剩餘所有token為空
        永久寶石 1綠
    """

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_buy_development_card_from_reserve(self) -> None:

        # given
        game = Game()
        player_a = Player()

        # 初始化玩家Ａ手中該有的token
        player_a.resource.diamond = 1
        player_a.resource.sapphire = 1
        player_a.resource.ruby = 1
        player_a.resource.onyx = 2
        # player_a.resource.gold = 1

        lv1_no11_card = DevelopmentCard(11, 1, 0, Resource(), Bonus())
        lv1_no11_card.bonus.emerald = 1
        lv1_no11_card.cost.diamond = 1
        lv1_no11_card.cost.sapphire = 1
        lv1_no11_card.cost.ruby = 1
        lv1_no11_card.cost.onyx = 2
        player_a.reserve_development_cards.append(lv1_no11_card)

        game.players = [player_a]

        # when
        player_a = game.players[0]
        development_card = player_a.reserve_development_cards[0]
        resource = player_a.choose_resource(diamond=1, sapphire=1, ruby=1, onyx=2)
        # resource = player_a.resource
        if game.check_can_buy(resource, development_card):
            player_a.buy_development_card_from_reserve(resource, development_card)

        # then
        self.assertEqual(player_a.resource.diamond, 0)
        self.assertEqual(player_a.resource.sapphire, 0)
        self.assertEqual(player_a.resource.ruby, 0)
        self.assertEqual(player_a.resource.onyx, 0)
        # self.assertEqual(player_a.resource.gold, 0)
        self.assertEqual(lv1_no11_card in player_a.reserve_development_cards, False) # 驗證改判斷該卡不存在保留發展卡中
        self.assertEqual(lv1_no11_card in player_a.development_cards, True)
        self.assertEqual(player_a.bonus.emerald, 1)
        

    def resource_to_tokens(self, resource: Resource) -> list[Token]:
        tokens = []
        for token in Token.__members__:
            token_counts = resource.__getattribute__(token)
            if token_counts > 0:
                for i in range(token_counts):
                    tokens.append(Token.__members__[token])
        return tokens
