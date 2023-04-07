from datetime import datetime
from functools import wraps

from flask import current_app, request, session
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request

from api.biz.account.business_account_service import BusinessAccountService
from api.biz.account.normal_account_service import NormalAccountService
from api.biz.error import AuthorizationError


def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "user_id" in session:
                return fn(*args, **kwargs)

            if "x-api-key" in request.headers:
                guest_key = request.headers["x-api-key"]
                if guest_key == "Guest":
                    session["user_id"] = "Guest"
                    session["email"] = None
                    session["account_type"] = None
                    session["plan"] = "Guest"
                    return fn(*args, **kwargs)

                return {
                    "return_code": -401,
                    "return_msg": "AuthenticationFailed: Is not a valid token.",
                    "return_data": []
                }

            if "Authorization" not in request.headers:
                raise AuthorizationError("Missing Authorization Token.")

            verify_jwt_in_request()
            jwt_data = get_jwt()

            for t in ["exp", "user_id", "account_type", "email"]:
                if t not in jwt_data:
                    return {
                        "return_code": -401,
                        "return_msg": "AuthenticationFailed: Is not a valid token.",
                        "return_data": []
                    }

            if datetime.now().timestamp() > jwt_data["exp"]:
                return {
                    "return_code": -402,
                    "return_msg": "AuthenticationFailed: Token timeout",
                    "return_data": []
                }
            if jwt_data["account_type"] == "normal":
                normal_account_service = NormalAccountService(current_app.userDBSession)
                user = normal_account_service.get_user(user_id=jwt_data["user_id"])
                if user:
                    session["user_id"] = jwt_data["user_id"]
                    session["email"] = jwt_data["email"]
                    session["account_type"] = jwt_data["account_type"]
                    session["plan"] = user["plan"]
                    return fn(*args, **kwargs)

                normal_account_service.add_user(user_id=jwt_data["user_id"], email=jwt_data["email"])
                session["user_id"] = jwt_data["user_id"]
                session["email"] = jwt_data["email"]
                session["account_type"] = jwt_data["account_type"]
                session["plan"] = "Free"
                return fn(*args, **kwargs)
            if jwt_data["account_type"] == "business":
                business_account_service = BusinessAccountService(current_app.userDBSession)
                user = business_account_service.get_user_by_user_id(jwt_data["user_id"])
                if user:
                    session["user_id"] = jwt_data["user_id"]
                    session["email"] = jwt_data["email"]
                    session["account_type"] = jwt_data["account_type"]
                    session["plan"] = user["plan"]
                    return fn(*args, **kwargs)

            return {
                "return_code": -401,
                "return_msg": "AuthenticationFailed: Is not a valid token.",
                "return_data": []
            }

        return decorator

    return wrapper
