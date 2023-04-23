from decimal import Decimal

from interface.api.common.number_utils import decimal_to_float, str_to_float
from tests.base_flask_test_case import BaseFlaskTestCase


class TestNumberUtils(BaseFlaskTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_decimal_to_float(self):
        test1 = None
        test2 = Decimal(123)
        test3 = "123"
        test4 = Decimal(12.3)

        self.assertEqual(None, decimal_to_float(test1))
        self.assertEqual(123.0, decimal_to_float(test2))
        self.assertEqual(None, decimal_to_float(test3))
        self.assertEqual(12.3, decimal_to_float(test4))

    def test_str_to_float(self):
        test1 = None
        test2 = "1123"
        test3 = "-1123"
        test4 = "-"
        test5 = "清倉"

        self.assertEqual(None, str_to_float(test1))
        self.assertEqual(1123.0, str_to_float(test2))
        self.assertEqual(-1123.0, str_to_float(test3))
        self.assertEqual("-", str_to_float(test4))
        self.assertEqual("清倉", str_to_float(test5))
