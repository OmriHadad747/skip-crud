from typing import Any, Dict
from flask import jsonify
from pydantic import validate_arguments
from werkzeug import security
from app.utils.errors import Errors as err
from skip_db_lib.database.freelancers import FreelancerDatabase as db
from skip_db_lib.models import freelancer as freelancer_model


# TODO catch more specifiec exceptions
# TODO do logs
# TODO write docstrings


class CrudFreelancer:
    @classmethod
    @validate_arguments
    def add_freelancer(cls, fields: Dict[str, Any]):
        try:
            new_freelancer = freelancer_model.Freelancer(**fields)
            new_freelancer.password = security.generate_password_hash(new_freelancer.password)

            if db.get_freelancer_by_email(new_freelancer.email):
                return err.already_exist_freelancer_with_email(new_freelancer.email)

            ack = db.add_freelancer(new_freelancer.dict())
            if not ack:
                return err.db_op_not_acknowledged(new_freelancer.dict(), op="insert")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"freelancer {new_freelancer.email} saved to db"), 201

    @classmethod
    @validate_arguments
    def get_customer_by_id(cls, id: str):
        freelancer = db.get_freelancer_by_id(id)
        if not freelancer:
            return err.id_not_found(id)

        return jsonify(freelancer=freelancer), 200

    @classmethod
    @validate_arguments
    def get_freelancer_by_email(cls, email: str):
        freelancer = db.get_freelancer_by_email(email)
        if not freelancer:
            return err.email_not_found(email)

        return jsonify(freelancer=freelancer), 200

    @classmethod
    @validate_arguments
    def update_freelancer(cls, email: str, fields: Dict[str, Any]):
        try:
            freelancer = freelancer_model.FreelancerUpdate(**fields)

            if freelancer.password:
                freelancer.password = security.generate_password_hash(freelancer.password)

            if not db.get_freelancer_by_email(email):
                return err.email_not_found(email)

            ack = db.update_freelancer(email, freelancer.dict(exclude_none=True))
            if not ack:
                return err.db_op_not_acknowledged(freelancer.dict(exclude_none=True), op="update")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"freelancer {email} updated in db"), 200

    @classmethod
    @validate_arguments
    def delete_freelancer(cls, email: str):
        try:
            if not db.get_freelancer_by_email(email):
                return err.email_not_found(email)

            ack = db.delete_freelancer(email)
            if not ack:
                return err.db_op_not_acknowledged({"freelancer_email": email}, op="delete")

        except Exception as e:
            return err.general_exception(e)

        return jsonify(msg=f"freelancer {email} deleted from db"), 200
