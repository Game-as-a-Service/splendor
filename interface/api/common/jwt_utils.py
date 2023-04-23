from functools import wraps


def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            return {
                "return_code": -401,
                "return_msg": "AuthenticationFailed: Is not a valid token.",
                "return_data": [],
            }

        return decorator

    return wrapper
