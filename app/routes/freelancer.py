from typing import Dict, Tuple
from flask import request, Response

# from flask_jwt_extended import jwt_required
from app.routes import freelancer_crud_bp
from app.services.freelancer import CrudFreelancer


@freelancer_crud_bp.post("/freelancer")
def add_freelancer() -> Tuple[Response, int]:
    return CrudFreelancer.add_freelancer(request.json)


@freelancer_crud_bp.get("/freelancer/<string:email>")
# @jwt_required()
def get_freelancer(email: str) -> Tuple[Response, int]:
    return CrudFreelancer.get_freelancer_by_email(email)


@freelancer_crud_bp.patch("/freelancer/<string:email>")
# @jwt_required()
def update_freelancer(email: str) -> Tuple[Response, int]:
    return CrudFreelancer.update_freelancer(email, request.json)


@freelancer_crud_bp.delete("/freelancer/<string:email>")
# @jwt_required()
def delete_freelancer(email: str) -> Tuple[Response, int]:
    return CrudFreelancer.delete_freelancer(email)
