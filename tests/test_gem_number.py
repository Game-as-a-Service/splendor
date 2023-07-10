
from unittest import TestCase
from domain.resource import Resource
from domain.game import Game
import pytest
from domain.resource import Token

@pytest.mark.parametrize(
    "player_num,gem_number",[(2,4),(3,5),(4,7)]
)

class TestGemNumber:
    def test_gem_number(self,player_num,gem_number):
        game = Game()
        game.start_game()
        # 玩家人數 2,3,4   gem_number4,5,7
        if len(game.players) == player_num:
            self.assertEqual(game.table.resource.diamond, gem_number)#鑽石 
            self.assertEqual(game.table.resource.sapphire, gem_number)#藍寶石
            self.assertEqual(game.table.resource.emerald, gem_number)#綠寶石
            self.assertEqual(game.table.resource.ruby, gem_number)#紅寶石
            self.assertEqual(game.table.resource.onyx, gem_number)#瑪瑙

