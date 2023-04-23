import json
from typing import Dict, List, Union

from flask import Response


def api_response(
    http_status: int = 200,
    data: Union[dict, list] = None,
    message: str = None,
    http_headers: Dict[str, Union[str, List[str]]] = None,
    **kwargs
) -> Response:
    """API Response"""
    http_status = int(http_status)
    payload = {**kwargs}
    if isinstance(data, (dict, list)):
        payload["data"] = data
    if message:
        payload["message"] = message

    http_headers = {**http_headers} if isinstance(http_headers, dict) else {}
    http_headers["Content-Type"] = "application/json; charset=utf-8"

    return Response(json.dumps(payload, ensure_ascii=False), http_status, http_headers)


def api_pagination_response(
    data: Union[list, dict],
    page: int,
    page_size: int,
    total: int,
    status: int = 200,
    updated_at: str = None,
    **kwargs
) -> Response:
    """API Response 分頁"""
    kwargs["page"] = page
    kwargs["total"] = total
    kwargs["pageSize"] = page_size
    if updated_at:
        kwargs["updatedAt"] = updated_at
    return api_response(status, data, **kwargs)
