from typing import Callable, Dict, Tuple

from app.handlers import hello_world
from core.models import HTTPRequest, HTTPResponse

routes: Dict[Tuple[str, str], Callable[[HTTPRequest], HTTPResponse]] = {
    ("GET", "/test"): hello_world
}

# prefix - os-dir mapping
static_routes: Dict[str, str] = {"/assets/": "app/assets/"}