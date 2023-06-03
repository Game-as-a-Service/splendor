from domain.player import Player
from domain.table import Table
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
        """happy path: player get 3 different tokens from table"""

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

    def _prepare_resource(self, resource_str: str) -> Resource:
        ret = Resource()
        for quantity, token in zip(resource_str, map(Token, Token.__members__)):
            ret.__setattr__(token.name, quantity)
            if int(quantity) > 0:
                for i in range(int(quantity)):
                    ret.token.append(token)
        return ret
