from werkzeug.test import TestResponse

from dbmodels.user_profile.nike_customer_info import NikeCustomerInfo
from tests import basic_user, basic_plan, test_watchlist, setup_basic_session
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiWatchlist(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self._clear_test_data()
        self.user_sql_session.add(NikeCustomerInfo(**{
            "user_id": basic_user,
            "plan": basic_plan,
            "status": "active",
            "watchlist": test_watchlist
        }))
        self.user_sql_session.flush()

    def _clear_test_data(self):
        self.user_sql_session.query(NikeCustomerInfo).filter(NikeCustomerInfo.user_id == basic_user).delete()
        self.user_sql_session.flush()
        self.cache.clear()

    def get_nike_customer_info_by_user_id(self, user_id: str) -> NikeCustomerInfo:
        return self.user_sql_session.query(NikeCustomerInfo) \
            .filter(NikeCustomerInfo.user_id == user_id) \
            .first()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.post('/watchlists')
            self.assertEqual(404, res.status_code)

    def test_it_should_200_when_add_watchlist(self):
        """增加追蹤清單，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.post('/watchlist', json={"name": "test2"})
            self.assertEqual(200, res.status_code)

            cus_info: NikeCustomerInfo = self.get_nike_customer_info_by_user_id(basic_user)
            watchlist = cus_info.watchlist
            self.assertEqual("test2", watchlist[1]["name"])

    def test_it_should_200_when_rename_watchlist(self):
        """重新命名追蹤清單，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.put('/watchlist/test', json={'name': 'rename'})
            self.assertEqual(200, res.status_code)

            cus_info: NikeCustomerInfo = self.get_nike_customer_info_by_user_id(basic_user)
            watchlist = cus_info.watchlist
            self.assertEqual(watchlist[0]["name"], "rename")

    def test_it_should_200_when_delete_watchlist(self):
        """刪除追蹤清單，應該回應200"""
        with self.app.test_client() as client:
            setup_basic_session(client)
            res: TestResponse = client.delete('/watchlist/test')
            self.assertEqual(200, res.status_code)

            cus_info: NikeCustomerInfo = self.get_nike_customer_info_by_user_id(basic_user)
            watchlist = cus_info.watchlist
            self.assertEqual(0, len(watchlist))
