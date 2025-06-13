from dataclasses import dataclass
from enum import Enum


class HTTPVersion(Enum):
    HTTP11 = "HTTP/1.1"


class Method(Enum):
    GET = "GET"
    POST = "POST"


class StatusCode(Enum):
    C_200_OK = (200, "OK")
    c_404_NOT_FOUND = (404, "Not Found")
    c_505_INTERNAL_SERVER_ERROR = (500, "Internal Server Error")

    @property
    def code(self) -> int:
        return self.value[0]

    @property
    def reason(self) -> str:
        return self.value[1]


@dataclass
class Header:
    field_name: str
    value: str


@dataclass
class Body:
    content: str | bytes


@dataclass
class RequestLine:
    method: Method
    request_uri: str
    http_version: HTTPVersion


@dataclass
class StatusLine:
    http_version: HTTPVersion
    status_code: StatusCode
    reason_phrase: str

    def get_status_line(self):
        return (
            self.http_version.value
            + " "
            + str(self.status_code.code)
            + " "
            + self.reason_phrase
        )


@dataclass
class HTTPRequest:
    request_line: RequestLine
    headers: list[Header]
    body: Body | None


@dataclass
class HTTPResponse:
    status_line: StatusLine
    headers: list[Header]
    body: Body
