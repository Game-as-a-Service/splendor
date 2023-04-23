from http import HTTPStatus
from logging import Logger
from typing import ClassVar, List, Optional


class BaseError(Exception):
    description = None
    code = None
    data = None
    http_status_code: HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, description, code=None, data=None):
        Exception.__init__(self, description)
        self.description = description
        self.code = code
        self.data = data


class AuthorizationError(BaseError):
    """Header Authorization 驗證失敗"""

    http_status_code = HTTPStatus.UNAUTHORIZED


class InvalidInvocation(BaseError):
    """缺少必要的呼叫資訊/或目前狀態不符"""

    http_status_code = HTTPStatus.BAD_REQUEST


class BusinessError(BaseError):
    """代表商務邏輯上的錯誤"""

    http_status_code = HTTPStatus.CONFLICT


class RateLimitingExceededError(BaseError):
    """代表某些限次的規則到達或超過上限"""

    http_status_code = HTTPStatus.TOO_MANY_REQUESTS


class DataValidationError(BaseError):
    """代表輸入的資料驗證不通過"""

    http_status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class InvalidPasswordError(BaseError):
    """代表密碼驗證不通過"""

    http_status_code = HTTPStatus.UNPROCESSABLE_ENTITY


class UserDataIntegrityError(BaseError):
    """目前代表用戶資料表的資料不完整"""

    http_status_code = HTTPStatus.CONFLICT


class DataNotFound(BaseError):
    """代表找不到某特定資料"""

    http_status_code = HTTPStatus.NOT_FOUND


class TenantDataConflictError(BaseError):
    """代表該操作不適用於當前用戶狀態"""

    http_status_code = HTTPStatus.CONFLICT


class TaskRunningError(BaseError):
    """Task 執行中, 尚未取得結果"""

    http_status_code = HTTPStatus.ACCEPTED


class TaskRunningForbidden(BaseError):
    """Task 執行中, 發生錯誤"""

    http_status_code = HTTPStatus.FORBIDDEN


class ServerError(BaseError):
    """Client 請求有效，Server 無法完成請求"""

    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR


def guard_valid_param(
    condition: any,
    err_msg: str,
    fill_errors: List[str] = None,
    logger: Optional[Logger] = None,
    extra_log_msg: str = None,
):
    guard_then_raise(
        condition, err_msg, InvalidInvocation, fill_errors, logger, extra_log_msg
    )


def guard_valid_data(
    condition: any,
    err_msg: str,
    fill_errors: List[str] = None,
    logger: Optional[Logger] = None,
    extra_log_msg: str = None,
):
    guard_then_raise(
        condition, err_msg, DataValidationError, fill_errors, logger, extra_log_msg
    )


def guard_business_rule(
    condition: any,
    err_msg: str,
    fill_errors: List[str] = None,
    logger: Optional[Logger] = None,
    extra_log_msg: str = None,
):
    guard_then_raise(
        condition, err_msg, BusinessError, fill_errors, logger, extra_log_msg
    )


def guard_then_raise(
    condition: any,
    err_msg: str,
    err_cls: ClassVar[Exception] = Exception,
    fill_errors: List[str] = None,
    logger: Optional[Logger] = None,
    extra_log_msg: str = None,
):
    if not condition:
        if isinstance(logger, Logger):
            logger.warning(
                err_msg if not extra_log_msg else f"{err_msg}, {extra_log_msg}"
            )

        if isinstance(fill_errors, list):
            fill_errors.append(err_msg)
            return
        raise err_cls(err_msg)
