from app.routes import routes, static_routes
from core.main import run_server
from framework.http_engine import HttpEngine

http_engine = HttpEngine(routes=routes, static_routes=static_routes)

run_server(http_engine=http_engine)
