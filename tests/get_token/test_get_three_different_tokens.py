from domain.game import Game
from domain.player import Player

# from domain.table import Table
from domain.resource import Resource, Token


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

    def test_get_three_different_tokens_case01(self) -> None:
        """happy path: successfully taken 3 different tokens"""

        # given
        game = Game()
        player_a = Player()
        # FIXME: avoid direct access instance variable
        # game.add_player(player_a)
        game.players = [player_a]
        game.table.resource.diamond = 2
        game.table.resource.sapphire = 4
        game.table.resource.emerald = 3
        # game.table.resource.token = [Token.diamond, Token.diamond, Token.sapphire, Token.sapphire, Token.sapphire, Token.sapphire, Token.emerald, Token.emerald, Token.emerald]
        game.table.resource.token = self.resource_to_tokens(game.table.resource)
        # for token in Token.__members__:
        #     token_counts = game.table.resource.__getattribute__(token)
        #     if token_counts > 0:
        #         for i in range(token_counts):
        #             game.table.resource.token.append(Token.__members__[token])

        # when
        taken_resource = Resource()
        taken_resource.diamond = 1
        taken_resource.sapphire = 1
        taken_resource.emerald = 1
        taken_resource.token = self.resource_to_tokens(taken_resource)

        game.get_token(player_a, taken_resource)

        # then
        self.assertEqual(player_a.resource.diamond, 1)
        self.assertEqual(player_a.resource.sapphire, 1)
        self.assertEqual(player_a.resource.emerald, 1)
        self.assertEqual(game.table.resource.diamond, 1)
        self.assertEqual(game.table.resource.sapphire, 3)
        self.assertEqual(game.table.resource.emerald, 2)

    def resource_to_tokens(self, resource: Resource) -> list[Token]:
        tokens = []
        for token in Token.__members__:
            token_counts = resource.__getattribute__(token)
            if token_counts > 0:
                for i in range(token_counts):
                    tokens.append(Token.__members__[token])
        return tokens
