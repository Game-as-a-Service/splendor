from requests import Response

from tests.base_flask_test_case import BaseFlaskTestCase


class TestHappyCase(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_it_should_200_when_api_is_alive(self):
        """玩家A購買10號LV1卡片"""
        playerA = Player()

        playerA.購買發展卡(LV=1,卡號=10,花費資源=資源.黑寶石)#資源.黑寶石=4

        分數=playerA.更新分數()
        資源=playerA.資源.黑寶石
        self.assertEqual(分數,1)
        self.assertEqual(資源,0)