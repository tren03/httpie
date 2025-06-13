import socket
from parser import build_request, build_response

from http_engine import HttpEngine, IHttpEngine
from models.models import HTTPRequest, HTTPResponse
from router import routes

HOST = "127.0.0.1"
PORT = 8888

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(4)
    print("*** WEB SERVER IS UP ***")
    conn, addr = s.accept()
    while conn:
        print(f"Connected to {addr}")
        headers = ""
        body = ""
        # request = conn.recv(1024)  # Read HTTP request

        # For a get request, there is no body
        # At this point, we have all the headers -> if post, then check content length, else continue
        while True:
            request = conn.recv(1024)
            parsed_request = request.decode()
            if "\r\n" in parsed_request:
                headers = headers + parsed_request
                break
            else:
                headers = headers + parsed_request

        raw_request = headers + "\r\n" + body
        http_request: HTTPRequest = build_request(raw_request=raw_request)
        http_response: HTTPResponse = HttpEngine(routes=routes).run(
            request=http_request
        )
        raw_response: str = build_response(response=http_response)

        # response = (
        #     "HTTP/1.1 200 OK\r\n"
        #     "Content-Type: text/plain\r\n"
        #     "Content-Length: 20\r\n"
        #     "\r\n"
        #     "Hello from my socket"
        # )
        conn.sendall(raw_response.encode())
