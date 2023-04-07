from werkzeug.test import TestResponse

from dbmodels.manager.video_info import VideoInfo
from tests.base_flask_test_case import BaseFlaskTestCase


class TestApiVideoInfo(BaseFlaskTestCase):
    def setUp(self) -> None:
        super().setUp()
        self._clear_test_data()
        self._prepare_test_data()

    def tearDown(self) -> None:
        self._clear_test_data()
        return super().tearDown()

    def _prepare_test_data(self):
        self.manager_sql_session.add(VideoInfo(**{
            "category": "market-analysis",
            "title": "dummy-title",
            "content": "dummy-content",
            "symbol": [
                "AAPL"
            ],
            "published_at": "2022-12-25",
            "photo_url": "https://photo-url/",
            "video_url": "https://vidoe-url/",
            "status": False
        }))
        self.manager_sql_session.flush()

    def _clear_test_data(self):
        self.manager_sql_session.query(VideoInfo) \
            .filter(VideoInfo.title == "dummy-title") \
            .delete()
        self.manager_sql_session.flush()

    def test_it_should_404_when_url_is_wrong(self):
        """URL錯誤，應該回應404"""
        with self.app.test_client() as client:
            res: TestResponse = client.get('/video/info/DUMMY')
            self.assertEqual(404, res.status_code)

    def test_it_should_400_when_parameter_is_wrong(self):
        """請求參數錯誤，應該回應400"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/video-info/123")
            self.assertEqual(400, res.status_code)

    def test_it_should_200_when_parameter_is_correct(self):
        """請求參數正確，應該回應200"""
        with self.app.test_client() as client:
            res: TestResponse = client.get("/video-info/market-analysis")
            self.assertEqual(200, res.status_code)

            self.assertEqual("market-analysis", res.json["data"][0]["category"])
            self.assertEqual("dummy-title", res.json["data"][0]["title"])
            self.assertEqual("dummy-content", res.json["data"][0]["content"])
            self.assertEqual(["AAPL"], res.json["data"][0]["symbol"])
            self.assertEqual("2022-12-25", res.json["data"][0]["publishedAt"])
            self.assertEqual("https://photo-url/", res.json["data"][0]["photoUrl"])
            self.assertEqual("https://vidoe-url/", res.json["data"][0]["videoUrl"])
            self.assertEqual(False, res.json["data"][0]["status"])

            res: TestResponse = client.get("/video-info/oriented-analysis")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])

            res: TestResponse = client.get("/video-info/finance-knowledge")
            self.assertEqual(200, res.status_code)
            self.assertEqual([], res.json["data"])
