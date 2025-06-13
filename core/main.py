import socket

from core.models import HTTPRequest, HTTPResponse
from core.parser import build_request, build_response
from framework.http_engine import HttpEngine

HOST = "127.0.0.1"
PORT = 8888


def run_server(host=HOST, port=PORT, http_engine: HttpEngine | None = None):
    if not HttpEngine:
        raise Exception("No http engine specified")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(4)
        print("*** WEB SERVER IS UP ***")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected to {addr}")
                headers = ""
                body = ""

                while True:
                    request = conn.recv(1024)
                    if not request:
                        break
                    parsed_request = request.decode()
                    headers += parsed_request
                    if "\r\n\r\n" in headers:
                        break

                raw_request = headers + "\r\n" + body
                print("REQ HEADERS", raw_request)
                print("REQ BODY", body)
                http_request: HTTPRequest = build_request(raw_request=raw_request)
                http_response: HTTPResponse = http_engine.run(request=http_request)
                raw_response: bytes = build_response(response=http_response)
                print("HTTP RESPONSE : \n", raw_response)
                conn.sendall(raw_response)
                print("closing connection")
