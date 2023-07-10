from unittest import TestCase
from domain.player import Player
from domain.game import start_gmae
from domain.game import Game

class NobleHaveThree(TestCase):
    def noble_have_three(self):
        
        game = Game()
        game.start_gmae()

        match len(game.players):
            case 2:
                self.assertEqual(len(game.table.nobles), 3)
            
            case 3:
                self.assertEqual(len(game.table.nobles), 4)

            case 4:
                self.assertEqual(len(game.table.nobles), 5)