from unittest import TestCase
from domain.resource import Resource
from domain.game import Game
class TestGoldToken(TestCase):
    # Test the number of gold tokens when the game starts
    def test_the_number_of_gold_tokens(self):
        game = Game()
        game.start()
        self.assertEqual(game.Resource.gold_token.number, 5)