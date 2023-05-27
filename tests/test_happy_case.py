from requests import Response

from tests.base_flask_test_case import BaseFlaskTestCase
from domain.Player import Player
from domain.Token import Token
from domain.DevelopmentCard import DevelopmentCard
from domain.Resource import Resource

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

    def test_player_buy_No10_lv1_card_success(self):
        # Given 玩家手中有4個黑色token
        player = Player()
        player.get_token(Token.onyx)
        player.get_token(Token.onyx)
        player.get_token(Token.onyx)
        player.get_token(Token.onyx)

        cost = Resource()
        cost.add_token(Token.onyx)
        cost.add_token(Token.onyx)
        cost.add_token(Token.onyx)
        cost.add_token(Token.onyx)

        card = DevelopmentCard(1, 10, 1, cost, Token.emerald)
        # When
        player.buy_development_card(card)
        # Then
        self.assertEqual(player.resource.black, 0)
        self.assertEqual(player.score, 1)
