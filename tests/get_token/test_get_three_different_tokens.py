from domain.game import Game
from domain.player import Player
from domain.table import Table
from domain.resource import Resource


from tests.base_flask_test_case import BaseFlaskTestCase


class TestGetThreeDifferentTokens(BaseFlaskTestCase):
    """test get three different tokens
    given:
        player A has empty resource
        table has resource: {diamond=2, sapphire=4, emerald=3}
    when:
        player A take 3 different tokens: {diamond=1, sapphire=1, emerald=1}
    then:
        player A has resource: {diamond=1, sapphire=1, emerald=1}
        table has resource: {diamond=1, sapphire=3, emerald=2}
    """

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_three_different_tokens_case01(self):
        """happy path: successfully taken 3 different tokens"""

        # given
        game = Game()
        player_a = Player(name="player A")
        game.add_player(player_a)
        game.table = Table(Resource(diamond=2, sapphire=4, emerald=3))

        # when
        game.get_token(player_a, Resource(diamond=1, sapphire=1, emerald=1))

        # then
        self.assertEqual(player_a.resource.diamond, 1)
        self.assertEqual(player_a.resource.sapphire, 1)
        self.assertEqual(player_a.resource.emerald, 1)
        self.assertEqual(game.table.resource.diamond, 1)
        self.assertEqual(game.table.resource.sapphire, 3)
        self.assertEqual(game.table.resource.emerald, 2)
