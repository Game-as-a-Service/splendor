from datetime import datetime, date

from api.common.datetime_utils import date_to_str, datetime_to_quarter, datetime_to_str, timestamp_to_datetime, \
    str_to_date
from tests.base_flask_test_case import BaseFlaskTestCase


class TestDatetimeUtils(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_date_to_str(self):
        test1 = None
        test2 = date(2022, 8, 1)
        test3 = datetime(2022, 8, 1, 12, 12, 12)
        test4 = "2022-08-01"
        test5 = "2022-08-01 12:12:12"

        self.assertEqual(None, date_to_str(test1))
        self.assertEqual("2022-08-01", date_to_str(test2))
        self.assertEqual("2022-08-01", date_to_str(test3))
        self.assertEqual(None, date_to_str(test4))
        self.assertEqual(None, date_to_str(test5))

    def test_datetime_to_str(self):
        test1 = None
        test2 = date(2022, 8, 1)
        test3 = datetime(2022, 8, 1, 12, 12, 12)
        test4 = "2022-08-01"
        test5 = "2022-08-01 12:12:12"

        self.assertEqual(None, datetime_to_str(test1))
        self.assertEqual(None, datetime_to_str(test2))
        self.assertEqual("2022-08-01 12:12:12", datetime_to_str(test3))
        self.assertEqual(None, datetime_to_str(test4))
        self.assertEqual(None, datetime_to_str(test5))

    def test_datetime_to_quarter(self):
        test1 = None
        test2 = date(2022, 8, 1)
        test3 = datetime(2022, 8, 1, 12, 12, 12)
        test4 = datetime(2022, 6, 30, 12, 12, 12)
        test5 = datetime(2022, 7, 1, 12, 12, 12)
        test6 = "2022-08-01"
        test7 = "2022-08-01 12:12:12"

        self.assertEqual(None, datetime_to_quarter(test1))
        self.assertEqual("2022 Q3", datetime_to_quarter(test2))
        self.assertEqual("2022 Q3", datetime_to_quarter(test3))
        self.assertEqual("2022 Q2", datetime_to_quarter(test4))
        self.assertEqual("2022 Q3", datetime_to_quarter(test5))
        self.assertEqual(None, datetime_to_quarter(test6))
        self.assertEqual(None, datetime_to_quarter(test7))

    def test_timestamp_to_datetime(self):
        test1 = None
        test2 = "1660024300"
        test3 = 1660024300

        self.assertEqual(None, timestamp_to_datetime(test1))
        self.assertEqual(None, timestamp_to_datetime(test2))
        self.assertEqual(datetime, type(timestamp_to_datetime(test3)))

    def test_str_to_date(self):
        test1 = None
        test2 = "2022-1-0"
        test3 = "2022111"
        test4 = "2022-01-01"
        test5 = "2022-01-01 12:00:00"

        self.assertEqual(None, str_to_date(test1))
        self.assertEqual(None, str_to_date(test2))
        self.assertEqual(None, str_to_date(test3))
        self.assertEqual(datetime(2022, 1, 1, 0, 0, 0), str_to_date(test4))
        self.assertEqual(datetime(2022, 1, 1, 12, 0, 0), str_to_date(test5, "%Y-%m-%d %H:%M:%S"))
