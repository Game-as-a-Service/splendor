import re
from decimal import Decimal
from typing import Optional


def decimal_to_float(num: Optional[Decimal]) -> Optional[float]:
    if num is None or not isinstance(num, Decimal):
        return None
    return float(num)


def str_to_float(num: Optional[str]) -> Optional[float]:
    if num is None or not isinstance(num, str):
        return None

    if re.search("\d", num) is None:  # noqa: W605
        return num

    return float(num)
