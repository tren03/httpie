from app.routes import routes
from core.main import run_server
from framework.http_engine import HttpEngine

http_engine = HttpEngine(routes=routes)

run_server(http_engine=http_engine)
