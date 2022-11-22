from typing import Any, Dict
from flask import jsonify
from pydantic import validate_arguments
from werkzeug import security

from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.database.customers import CustomerDatabase as db
from skip_common_lib.models import customer as customer_model


# TODO catch more specifiec exceptions
# TODO do logs
# TODO write docstrings
# TODO type all the returnes of the function


class CrudCustomer:
    @classmethod
    @validate_arguments
    def add_customer(cls, fields: Dict[str, Any]):
        try:
            new_customer = customer_model.Customer(**fields)
            new_customer.password = security.generate_password_hash(new_customer.password)

            if db.get_customer_by_email(new_customer.email):
                return err.already_exist_customer_with_email(new_customer.email)

            ack = db.add_customer(new_customer.dict())
            if not ack:
                return err.db_op_not_acknowledged(new_customer.dict(), op="insert")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"customer {new_customer.email} saved to db"), 201

    @classmethod
    @validate_arguments
    def get_customer_by_id(cls, id: str):
        customer = db.get_customer_by_id(id)
        if not customer:
            return err.id_not_found(id)

        return jsonify(customer=customer), 200

    @classmethod
    @validate_arguments
    def get_customer_by_email(cls, email: str):
        customer = db.get_customer_by_email(email)
        if not customer:
            return err.email_not_found(email)

        return jsonify(customer=customer), 200

    @classmethod
    @validate_arguments
    def update_customer(cls, email: str, fields: Dict[str, Any]):
        try:
            customer = customer_model.CustomerUpdate(**fields)

            if customer.password:
                customer.password = security.generate_password_hash(customer.password)

            if not db.get_customer_by_email(email):
                return err.email_not_found(email)

            ack = db.update_customer(email, customer.dict(exclude_none=True))
            if not ack:
                return err.db_op_not_acknowledged(customer.dict(exclude_none=True), op="update")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"customer {email} updated in db"), 200

    @classmethod
    @validate_arguments
    def delete_customer(cls, email: str):
        try:
            if not db.get_customer_by_email(email):
                return err.email_not_found(email)

            ack = db.delete_customer(email)
            if not ack:
                return err.db_op_not_acknowledged({"customer_email": email}, op="delete")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"customer {email} deleted from db"), 200
