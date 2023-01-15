import logging

from pydantic import validate_arguments
from werkzeug import security

from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.database.freelancers import FreelancerDB as db
from skip_common_lib.schemas import freelancer as freelancer_schema
from skip_common_lib.schemas import response as resp_schema


class CrudFreelancer:
    logger = logging.getLogger("skip-crud-service")

    @classmethod
    @validate_arguments
    async def get_freelancer_by_id(cls, id: str):
        cls.logger.debug(f"retrieveing freelancer by id {id}")

        freelancer = await db.get_freelancer_by_id(id)
        if not freelancer:
            return err.id_not_found(id, cls.logger)

        return resp_schema.EntityResponse(args=dict(id=id), output=freelancer)

    @classmethod
    @validate_arguments
    async def get_freelancer_by_email(cls, email: str):
        cls.logger.debug(f"retrieveing freelancer by email {email}")

        freelancer = await db.get_freelancer_by_email(email)
        if not freelancer:
            return err.email_not_found(email, cls.logger)

        return resp_schema.EntityResponse(args=dict(email=email), entity=freelancer)

    @classmethod
    @validate_arguments
    async def add_freelancer(cls, new_freelancer: freelancer_schema.Freelancer):
        cls.logger.debug(f"adding freelancer {new_freelancer.dict()}")

        try:
            new_freelancer.password = security.generate_password_hash(new_freelancer.password)

            if await db.get_freelancer_by_email(new_freelancer.email):
                return err.already_exist_freelancer_with_email(new_freelancer.email)

            res = await db.add_freelancer(new_freelancer)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(
                    new_freelancer.dict(exclude_none=True), op="insert", logger=cls.logger
                )

        except Exception as e:
            # TODO catch more specifiec exceptions here
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=new_freelancer.dict(), msg=f"freelancer {new_freelancer.email} saved to db"
        )

    @classmethod
    @validate_arguments
    async def update_freelancer(cls, email: str, freelancer: freelancer_schema.FreelancerUpdate):
        try:
            cls.logger.debug(
                f"udpating freelancer {email} with fields {freelancer.dict(exclude_none=True)}"
            )

            if freelancer.password:
                freelancer.password = security.generate_password_hash(freelancer.password)

            if not await db.get_freelancer_by_email(email):
                return err.email_not_found(email, cls.logger)

            res = await db.update_freelancer(email, freelancer)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(
                    freelancer.dict(exclude_none=True), op="update", logger=cls.logger
                )

        except Exception as e:
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=freelancer.dict(exclude_none=True), msg=f"freelancer {email} updated in db"
        )

    @classmethod
    @validate_arguments
    async def delete_freelancer(cls, email: str):
        cls.logger.debug(f"deleting freelancer {email}")

        try:
            if not await db.get_freelancer_by_email(email):
                return err.email_not_found(email, cls.logger)

            res = await db.delete_freelancer(email)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(
                    {"freelancer_email": email}, op="delete", logger=cls.logger
                )

        except Exception as e:
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=dict(email=email), msg=f"freelancer {email} deleted from db"
        )
