from flask import Flask
from flask_restful import Api

from config.api_config import Config
from interface.api.routes.account.api_user_profile import ApiUserProfile
from interface.api.routes.api_home import ApiHome
from interface.api.routes.api_preview import ApiPreview
from interface.api.routes.open_api_spec import OpenApiSpec


def setup_routes(app: Flask):
    if Config.ENV_SET.lower() in ["dev", "local"]:

        @app.route("/open-api-spec", defaults={"path": None})
        @app.route("/open-api-spec/", defaults={"path": None})
        @app.route("/open-api-spec/<path:path>")
        def send_open_api_spec(path: str):
            return OpenApiSpec.resolve_content(path)

    api = Api(app)
    api.add_resource(ApiHome, "/")
    api.add_resource(ApiPreview, "/preview")

    # User 相關
    api.add_resource(ApiUserProfile, "/user", "/user/<user_id>")
