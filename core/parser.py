from core.models import (
    Body,
    Header,
    HTTPRequest,
    HTTPResponse,
    HTTPVersion,
    Method,
    RequestLine,
)


def build_request(raw_request: str) -> HTTPRequest:
    head, body_part = raw_request.split("\r\n\r\n", 1)
    lines = head.split("\r\n")

    # Parse request line
    raw_request_line = lines[0]
    method_str, request_uri, http_version_str = raw_request_line.split(" ")

    # Dynamically parse method and HTTP version
    try:
        method = Method(method_str)
    except ValueError:
        raise ValueError(f"Unsupported HTTP method: {method_str}")

    try:
        http_version = HTTPVersion(http_version_str)
    except ValueError:
        raise ValueError(f"Unsupported HTTP version: {http_version_str}")

    request_line = RequestLine(
        method=method, request_uri=request_uri, http_version=http_version
    )

    # Parse headers
    headers = []
    for line in lines[1:]:
        if not line.strip():
            continue
        try:
            key, value = line.split(":", 1)
            headers.append(Header(field_name=key.strip(), value=value.strip()))
        except ValueError:
            raise ValueError(f"Malformed header line: {line}")

    # Parse body
    body = Body(content=body_part) if body_part else None

    return HTTPRequest(request_line=request_line, headers=headers, body=body)


def build_response(response: HTTPResponse) -> str:
    status_line = response.status_line.get_status_line()
    headers = "\r\n".join(
        f"{header.field_name}: {header.value}" for header in response.headers
    )
    body = response.body.content if response.body else ""

    return f"{status_line}\r\n{headers}\r\n\r\n{body}"
