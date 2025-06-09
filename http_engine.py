from typing import Callable, Protocol

from models.models import Header, HTTPRequest, HTTPResponse
from router import not_found


class IHttpEngine(Protocol):
    def run(self, request: HTTPRequest) -> HTTPResponse:
        raise NotImplementedError()


class HttpEngine(IHttpEngine):
    def __init__(
        self, routes: dict[tuple[str, str], Callable[[HTTPRequest], HTTPResponse]]
    ):
        self.router = routes

    def run(self, request: HTTPRequest) -> HTTPResponse:
        method = request.request_line.method.value
        path = request.request_line.request_uri
        route_key = (method, path)

        if route_key in self.router:
            handler: Callable[[HTTPRequest], HTTPResponse] = self.router[route_key]
            return handler(request)
        else:
            return not_found()
