from typing import Tuple
from flask import request, Response

from app.routes import login_bp
from app.services.login import Login


@login_bp.post("/login")
def login() -> Tuple[Response, int]:
    return Login.login(request.json)
