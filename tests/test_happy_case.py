from requests import Response

from domain.bonus import Bonus
from domain.card import DevelopmentCard
from domain.player import Player
from domain.resource import Resource, Token
from tests.base_flask_test_case import BaseFlaskTestCase


class TestHappyCase(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_200_when_api_is_alive(self):
        """API狀態正常，應該回應200"""
        with self.app.test_client() as client:
            res: Response = client.get("/")
            self.assertEqual(200, res.status_code)
            self.assertEqual("API is alive.", res.json["message"])

    def test玩家用4個黑寶石購買10號lv1卡片(self):
        p = Player()
        p.resource.存錢(Token.onyx)
        p.resource.存錢(Token.onyx)
        p.resource.存錢(Token.onyx)
        p.resource.存錢(Token.onyx)
        cost = Resource()  # 4個黑寶石
        cost.onyx = 4
        bonus = Bonus()  # 無獎勵
        bonus.emerald = 1
        card = DevelopmentCard(10, 1, 1, cost, bonus)  # 10號lv1卡片
        # When   #####################################
        p.buy_development_card(cost, card)
        # Then   #####################################
        self.assertEqual(1, p.score)
        self.assertEqual(1, len(p.development_cards))
        self.assertEqual(0, p.resource.onyx)
