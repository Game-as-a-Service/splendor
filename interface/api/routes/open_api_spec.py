import json
import os

import yaml
from dollar_ref import resolve_file
from flask import Response, request, send_from_directory
from werkzeug.exceptions import NotFound


class OpenApiSpec:
    location = os.path.realpath(
        os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "open-api-spec")
    )

    @classmethod
    def resolve_content(cls, path: str or None) -> Response:
        request_path = request.path
        path = "" if not path else path
        abs_path = os.path.join(cls.location, path)
        if os.path.isdir(abs_path):
            if not request_path.endswith("/"):
                # redirect trail slash
                return Response(status=301, headers={"Location": request_path + "/"})
            path = cls._resolve_index_file_path(path)
            abs_path = os.path.join(cls.location, path)
        if not os.path.isfile(abs_path):
            raise NotFound("Resource {} not found".format(request.path))

        if abs_path.endswith((".yaml", ".yml", ".json")):
            resolved = resolve_file(abs_path, cwd=os.path.dirname(abs_path))
            if abs_path.endswith(".json"):
                return Response(
                    json.dumps(resolved, ensure_ascii=False),
                    200,
                    {"Content-Type": "application/json"},
                )

            return Response(
                yaml.dump(resolved, allow_unicode=True, encoding="utf-8"),
                200,
                {"Content-Type": "application/yaml"},
            )

        return send_from_directory(cls.location, path)

    @classmethod
    def _resolve_index_file_path(cls, path) -> str:
        for f in ["index.html", "index.htm"]:
            abs_path = os.path.join(cls.location, path, f)
            if os.path.isfile(abs_path):
                return os.path.join(path, f)
        return path
