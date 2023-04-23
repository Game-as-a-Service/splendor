from datetime import date, datetime
from typing import Optional


def date_to_str(value: Optional[date], fmt: str = "%Y-%m-%d") -> Optional[str]:
    if value is None or not isinstance(value, date):
        return None
    return datetime.strftime(value, fmt)


def datetime_to_str(value: Optional[datetime]) -> Optional[str]:
    if value is None or not isinstance(value, datetime):
        return None
    return datetime.strftime(value, "%Y-%m-%d %H:%M:%S")


def datetime_to_week(value: Optional[date]) -> Optional[str]:
    if value is None or not isinstance(value, date):
        return None
    return datetime.strftime(value, "%W")


def datetime_to_quarter(value: Optional[date]) -> Optional[str]:
    if value is None or not isinstance(value, date):
        return None
    return f"{value.year} Q{(value.month - 1) // 3 + 1}"


def timestamp_to_datetime(timestamp: Optional[int]) -> Optional[datetime]:
    if timestamp is None or not isinstance(timestamp, int):
        return None
    return datetime.fromtimestamp(timestamp)


def str_to_date(value: Optional[str], fmt: str = "%Y-%m-%d") -> Optional[date]:
    if value is None or not isinstance(value, str):
        return None

    try:
        datetime.strptime(value, fmt)
    except ValueError:
        return None

    return datetime.strptime(value, fmt)
