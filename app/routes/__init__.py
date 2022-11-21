from flask import Blueprint


job_crud_bp = Blueprint("job_crud_bp", "job")

customer_crud_bp = Blueprint("customer_crud_bp", "customer")

freelancer_crud_bp = Blueprint("freelancer_crud_bp", "freelancer")

login_bp = Blueprint("login", "login")
