from typing import Dict, Tuple
from flask import request
from app.routes import login_bp
from app.services.login import Login


@login_bp.post("/login")
def login() -> Tuple[Dict, int]:
    return Login.login(request.json)
