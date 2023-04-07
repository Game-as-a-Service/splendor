from unittest.mock import patch

from werkzeug.test import TestResponse

from api.biz.account.tradingview_account_service import TradingviewAccountService
from dbmodels.nike.tradingview_account_list import TradingviewAccountList
from tests import setup_guest_session, setup_free_session, setup_basic_session, setup_business_session, basic_user, \
    business_user
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiTradingviewAccount(BaseFlaskTestCase):

    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        return

    def _clear_test_data(self):
        self.nike_sql_session.execute("""TRUNCATE TABLE tradingview_account_list;""")
        self.nike_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.post('/tradingview/accounts', json={})
            self.assertEqual(404, res.status_code)

    def test_it_should_409_when_permission_invalid(self):
        """用戶權限不足，應該回應409"""
        with self.app.test_client() as client:
            setup_guest_session(client)
            payload = {"tradingviewAccount": "account"}
            res: TestResponse = client.post('/tradingview/account', json=payload)
            self.assertEqual(409, res.status_code)

            setup_free_session(client)
            payload = {"tradingviewAccount": "account"}
            res: TestResponse = client.post('/tradingview/account', json=payload)
            self.assertEqual(409, res.status_code)

    def test_it_should_422_when_payload_not_correct(self):
        """Payload不正確，應該回應422"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            payload = {"tradingviewAccounts": "account"}
            res: TestResponse = client.post('/tradingview/account', json=payload)
            self.assertEqual(422, res.status_code)

    def test_it_should_200_when_db_not_data_and_update_data(self):
        """DB沒有資料，可以成功寫入，應該回應200"""
        with patch.object(TradingviewAccountService, '_discord_hook', return_value=None) as mocked_discord:
            with self.app.test_client() as client:
                self._clear_test_data()
                setup_basic_session(client)
                payload = {"tradingviewAccount": "tradingview-id-1"}
                res: TestResponse = client.post('/tradingview/account', json=payload)
                self.assertEqual(200, res.status_code)

                account: TradingviewAccountList = self.nike_sql_session.query(TradingviewAccountList) \
                    .filter(TradingviewAccountList.user_id == basic_user) \
                    .first()

                self.assertEqual(basic_user, account.user_id)
                self.assertEqual(payload["tradingviewAccount"], account.tradingview_account)
                self.assertEqual(None, account.last_tradingview_account)
            mocked_discord.assert_called()

    def test_it_should_200_when_update_data(self):
        """DB有資料，可以成功更新，應該回應200"""
        with patch.object(TradingviewAccountService, '_discord_hook', return_value=None) as mocked_discord:
            with self.app.test_client() as client:
                self._clear_test_data()
                setup_business_session(client)
                self.nike_sql_session.add(TradingviewAccountList(**{
                    "user_id": business_user,
                    "tradingview_account": "tradingview-id-1"
                }))
                self.nike_sql_session.flush()

                payload = {"tradingviewAccount": "tradingview-id-2"}
                res: TestResponse = client.post('/tradingview/account', json=payload)
                self.assertEqual(200, res.status_code)

                account: TradingviewAccountList = self.nike_sql_session.query(TradingviewAccountList) \
                    .filter(TradingviewAccountList.user_id == business_user) \
                    .first()

                self.assertEqual(business_user, account.user_id)
                self.assertEqual(payload["tradingviewAccount"], account.tradingview_account)
                self.assertEqual("tradingview-id-1", account.last_tradingview_account)
            mocked_discord.assert_called()
