from requests import Response
from tests.base_flask_test_case import BaseFlaskTestCase
from domain.player import Player
from domain.game import Game

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
        PlayerA = Player()
        PlayerB = Player()
        
        #when
        Game1 = Game()
        Game1.startGame()
        
        #then
        for _ in range(4):
            Game1.draw_card1()
            Game1.draw_card2()
            Game1.draw_card3()

        self.assertEqual(len(Game1.table.card1),4)
        self.assertEqual(len(Game1.table.card2),4)
        self.assertEqual(len(Game1.table.card3),4)


        