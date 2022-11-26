from flask import jsonify
from pydantic import validate_arguments
from werkzeug import security

from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.database.freelancers import FreelancerDB as db
from skip_common_lib.schemas import freelancer as freelancer_schema
from skip_common_lib.schemas import response as resp_schema


# TODO catch more specifiec exceptions
# TODO do logs


class CrudFreelancer:
    @classmethod
    @validate_arguments
    async def get_freelancer_by_id(cls, id: str):
        freelancer = await db.get_freelancer_by_id(id)
        if not freelancer:
            return err.id_not_found(id)

        return resp_schema.EntityResponse(args={"id": id}, output=freelancer)

    @classmethod
    @validate_arguments
    async def get_freelancer_by_email(cls, email: str):
        freelancer = await db.get_freelancer_by_email(email)
        if not freelancer:
            return err.email_not_found(email)

        return resp_schema.EntityResponse(args={"email": email}, entity=freelancer)

    @classmethod
    @validate_arguments
    async def add_freelancer(cls, new_freelancer: freelancer_schema.Freelancer):
        try:
            new_freelancer.password = security.generate_password_hash(new_freelancer.password)

            if await db.get_freelancer_by_email(new_freelancer.email):
                return err.already_exist_freelancer_with_email(new_freelancer.email)

            res = await db.add_freelancer(new_freelancer.dict())
            if not res.acknowledged:
                return err.db_op_not_acknowledged(
                    new_freelancer.dict(exclude_none=True), op="insert"
                )

        except Exception as e:
            return err.general_exception(e)

        return resp_schema.MsgResponse(
            args=new_freelancer.dict(),
            msg=f"freelancer {new_freelancer.email} saved to db"
        )

    @classmethod
    @validate_arguments
    async def update_freelancer(cls, email: str, freelancer: freelancer_schema.FreelancerUpdate):
        try:
            if freelancer.password:
                freelancer.password = security.generate_password_hash(freelancer.password)

            if not await db.get_freelancer_by_email(email):
                return err.email_not_found(email)

            ack = await db.update_freelancer(email, freelancer.dict(exclude_none=True))
            if not ack:
                return err.db_op_not_acknowledged(freelancer.dict(exclude_none=True), op="update")

        except Exception as e:
            return err.general_exception(e)

        return resp_schema.MsgResponse(
            args=freelancer.dict(),
            msg=f"freelancer {email} updated in db"
        )

    @classmethod
    @validate_arguments
    async def delete_freelancer(cls, email: str):
        try:
            if not await db.get_freelancer_by_email(email):
                return err.email_not_found(email)

            ack = await db.delete_freelancer(email)
            if not ack:
                return err.db_op_not_acknowledged({"freelancer_email": email}, op="delete")

        except Exception as e:
            return err.general_exception(e)

        return resp_schema.MsgResponse(
            args={"email": email},
            msg=f"freelancer {email} deleted from db"
        )
