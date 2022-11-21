from typing import Tuple
from flask import request, Response

# from flask_jwt_extended import jwt_required
from app.routes import customer_crud_bp
from app.services.customer import CrudCustomer
from app.services.job import CrudJob


# TODO type all the returns of the functions here


@customer_crud_bp.post("/customer")
def add_customer() -> Tuple[Response, int]:
    return CrudCustomer.add_customer(request.json)


@customer_crud_bp.get("/customer/<string:email>")
# @jwt_required()
def get_customer(email: str) -> Tuple[Response, int]:
    return CrudCustomer.get_customer_by_email(email)


@customer_crud_bp.patch("/customer/<string:email>")
# @jwt_required()
def update_customer(email: str) -> Tuple[Response, int]:
    return CrudCustomer.update_customer(email, request.json)


@customer_crud_bp.delete("/customer/<string:email>")
# @jwt_required()
def delete_customer(email: str) -> Tuple[Response, int]:
    return CrudCustomer.delete_customer(email)


@customer_crud_bp.post("/customer/job")
def post_job() -> Tuple[Response, int]:
    return CrudJob.post_job(request.json)
