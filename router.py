from typing import Callable, Dict, Tuple
from models.models import (
    HTTPRequest,
    HTTPResponse,
    StatusLine,
    HTTPVersion,
    StatusCode,
    Header,
    Body,
)


def hello_world(request: HTTPRequest) -> HTTPResponse:
    status_line = StatusLine(
        http_version=HTTPVersion.HTTP11,
        status_code=StatusCode.C_200_OK,
        reason_phrase=StatusCode.C_200_OK.reason,
    )
    headers = [
        Header(field_name="Content-Type", value="text/plain"),
        Header(field_name="Content-Length", value=str(len("Hello, world!"))),
    ]
    body = Body(content="Hello, world!")
    return HTTPResponse(status_line=status_line, headers=headers, body=body)


def not_found() -> HTTPResponse:
    status_line = StatusLine(
        http_version=HTTPVersion.HTTP11,
        status_code=StatusCode.c_404_NOT_FOUND,
        reason_phrase=StatusCode.c_404_NOT_FOUND.reason,
    )
    body_content = "404 Not Found"
    headers = [
        Header(field_name="Content-Type", value="text/plain"),
        Header(field_name="Content-Length", value=str(len(body_content))),
    ]
    body = Body(content=body_content)
    return HTTPResponse(status_line=status_line, headers=headers, body=body)


routes: Dict[Tuple[str, str], Callable[[HTTPRequest], HTTPResponse]] = {
    ("GET", "/test"): hello_world
}
