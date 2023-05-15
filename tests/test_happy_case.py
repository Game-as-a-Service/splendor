from requests import Response
from tests.base_flask_test_case import BaseFlaskTestCase
from domain.player import Player
from domain.resource import Resource
from domain.token import Token
from domain.developmentcard import Developmentcard

class TestApiHome(BaseFlaskTestCase):
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

    def test(self):
        #given
        player1 = Player()
        player1.get_token(Token.onyx)
        player1.get_token(Token.onyx)
        player1.get_token(Token.onyx)
        player1.get_token(Token.onyx)

        cost = []
        cost.append(Token.onyx)
        cost.append(Token.onyx)
        cost.append(Token.onyx)
        cost.append(Token.onyx)
        
        card = Developmentcard(10,1,cost,1,Token.emerald)
        #when
        player1.buy_developmentcard(card)
        #then
        self.assertEqual(player1.resource.black,0)
        self.assertEqual(player1.score,1)
        
        

