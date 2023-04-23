from flask import request
from flask_restful import Resource
from requests import Response
from sqlalchemy import inspect

from interface.api.common.error import InvalidInvocation
from interface.api.common.response_utils import api_response
from interface.api.containers.decorator import inject_service
from interface.repository.mySQL.account.user_info_service import UserInfoService


class ApiUserProfile(Resource):
    @inject_service()
    def __init__(
        self,
        user_info_service: UserInfoService,
    ) -> None:
        self._user_info_service = user_info_service

    def get(self) -> Response:
        user_id = request.args.get("userId")
        data = self._user_info_service.get_user_info_by_user_id(user_id)
        data = {
            "userId": data.user_id,
            "name": data.name,
        }
        if not data:
            raise InvalidInvocation("user is not exists.")

        return api_response(data=data, message="Success")

    def post(self) -> Response:
        data = request.get_json()["data"]
        user_id = data.get("userId")
        name = data.get("name")
        self._user_info_service.add_user_info(user_id, name)
        return api_response(data=data, message="Success")

    @staticmethod
    def object_as_dict(obj):
        res = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
        return res
