from typing import Any, Dict
from werkzeug import security
from flask import jsonify
from flask_jwt_extended import create_access_token

from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.database.customers import CustomerDatabase as db


class Login:
    @classmethod
    def login(cls, req_body: Dict[str, Any]):
        email = req_body.get("email")
        password = req_body.get("password")

        customer: Dict = db.get_customer_by_email(email)

        if not security.check_password_hash(customer.get("password", ""), password):
            return err.login_failed(), 401  # unauthorized

        return jsonify(access_token=create_access_token(identity=customer))
