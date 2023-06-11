from domain.player import Player
from domain.table import Table
from domain.resource import Resource, Token
from tests.base_flask_test_case import BaseFlaskTestCase


class TestGetThreeDifferentTokens(BaseFlaskTestCase):
    """test get three different tokens
    case01: (happy path) player get 3 different tokens from table
    case02: player can get 2 or less different tokens from table if table has only 2 or less different tokens
    case03: invalid action if player request token that table don't exist
    case04: invalid action if player request 4 or more tokens
    case05: invalid action if player request 2 or less different tokens while table has 3 or more different tokens
    case06: invalid action if player request 0 token
    """

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_three_different_tokens_case01(self) -> None:
        """happy path: player get 3 different tokens from table

        given:
            player A has empty resource
            table has resource: {diamond=2, sapphire=4, emerald=3}
        when:
            player A take 3 different tokens: {diamond=1, sapphire=1, emerald=1}
        then:
            player A has resource: {diamond=1, sapphire=1, emerald=1}
            table has resource: {diamond=1, sapphire=3, emerald=2}
        """

        # given
        player_a = Player()
        table = Table()
        table.resource = self._prepare_resource("243")
        taken_resource = self._prepare_resource("111")

        # when
        player_a.get_token(taken_resource, table)

        # then
        self.assertEqual(player_a.resource.diamond, 1)
        self.assertEqual(player_a.resource.sapphire, 1)
        self.assertEqual(player_a.resource.emerald, 1)
        self.assertEqual(table.resource.diamond, 1)
        self.assertEqual(table.resource.sapphire, 3)
        self.assertEqual(table.resource.emerald, 2)

    def test_get_three_different_tokens_case02(self) -> None:
        """player can get 2 or less different tokens from table if table has only 2 or less different tokens

        given:
            player A has empty resource
            table has resource: {diamond=2, sapphire=4}
        when:
            player A take 2 different tokens: {diamond=1, sapphire=1}
        then:
            player A has resource: {diamond=1, sapphire=1}
            table has resource: {diamond=1, sapphire=3}
        """

        # given
        player_a = Player()
        table = Table()
        table.resource = self._prepare_resource("24")
        taken_resource = self._prepare_resource("11")

        # when
        player_a.get_token(taken_resource, table)

        # then
        self.assertEqual(player_a.resource.diamond, 1)
        self.assertEqual(player_a.resource.sapphire, 1)
        self.assertEqual(table.resource.diamond, 1)
        self.assertEqual(table.resource.sapphire, 3)

    def test_get_three_different_tokens_case03(self) -> None:
        """invalid action if player request token that table don't exist

        given:
            player A has empty resource
            table has resource: {diamond=2, sapphire=4}
        when:
            player A take 3 different tokens: {diamond=1, sapphire=1, emerald=1}
        then:
            get exception with emerald because table do not have emerald
        """

        # given
        player_a = Player()
        table = Table()
        table.resource = self._prepare_resource("24")
        taken_resource = self._prepare_resource("111")

        # when
        with self.assertRaises(Exception) as cm:
            player_a.get_token(taken_resource, table)

        # then
        the_exception = cm.exception
        self.assertIn(Token.emerald.value, the_exception.__str__().split())

    def _prepare_resource(self, resource_str: str) -> Resource:
        ret = Resource()
        for quantity, token in zip(resource_str, map(Token, Token.__members__)):
            ret.__setattr__(token.name, quantity)
            if int(quantity) > 0:
                for _ in range(int(quantity)):
                    ret.token.append(token)
        return ret
