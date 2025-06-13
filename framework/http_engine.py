import mimetypes
import os
from typing import Callable, Protocol

from app.handlers import not_found
from core.models import (
    Body,
    Header,
    HTTPRequest,
    HTTPResponse,
    HTTPVersion,
    StatusCode,
    StatusLine,
)


class IHttpEngine(Protocol):
    def run(self, request: HTTPRequest) -> HTTPResponse:
        raise NotImplementedError()


class HttpEngine(IHttpEngine):
    def __init__(
        self,
        routes: dict[tuple[str, str], Callable[[HTTPRequest], HTTPResponse]],
        static_routes: dict[str, str],
    ):
        self.router = routes
        self.static_routes = static_routes

    def run(self, request: HTTPRequest) -> HTTPResponse:
        method = request.request_line.method.value
        path = request.request_line.request_uri
        route_key = (method, path)
        static_response = static_file_handler(route_key=route_key, static_routes=self.static_routes)
        if static_response:
            return static_response
        if route_key in self.router:
            handler: Callable[[HTTPRequest], HTTPResponse] = self.router[route_key]
            return handler(request)
        else:
            return not_found()


def static_file_handler(
    route_key: tuple[str, str],
    static_routes: dict[str, str],
) -> HTTPResponse | None:
    method, path = route_key
    for url_prefix, dir_path in static_routes.items():
        if path.startswith(url_prefix):
            relative_path = path[len(url_prefix) :]
            file_path = os.path.join(dir_path, relative_path)

            if os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(url=file_path)
                content_type = (
                    mime_type or "application/octet-stream"
                )  # fall back to octet-stream based on RFC
                with open(file_path, "rb") as f:
                    content = f.read()
                print("CONTENT", content)
                return build_static_response(
                    body_content=content, mime_type=content_type
                )
            else:
                return not_found()
    return None


def build_static_response(body_content: bytes, mime_type: str) -> HTTPResponse:
    status_line = StatusLine(
        http_version=HTTPVersion.HTTP11,
        status_code=StatusCode.C_200_OK,
        reason_phrase=StatusCode.C_200_OK.reason,
    )
    headers = [
        Header(field_name="Content-Type", value=mime_type),
        Header(field_name="Content-Length", value=str(len(body_content))),
        Header(field_name="Connection", value="close"),
    ]
    body_content = body_content
    body = Body(content=body_content)
    return HTTPResponse(status_line=status_line, headers=headers, body=body)
