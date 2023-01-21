import logging

from pydantic import validate_arguments
from werkzeug import security

from app.schemas.freelancer import Freelancer, FreelancerUpdate
from app.schemas.response import MsgResp, EntityResp
from app.schemas.request import NearestFilterReq
from app.database.freelancer import FreelancerDB as db
from app.errors import Errors as err


class CrudFreelancer:
    logger = logging.getLogger("crud-service")

    @classmethod
    @validate_arguments
    async def get_freelancer_by_id(cls, id: str) -> EntityResp:
        cls.logger.debug(f"retrieveing freelancer by id {id}")

        freelancer = await db.get_freelancer_by_id(id)
        if not freelancer:
            return err.id_not_found(id, cls.logger)

        return EntityResp(entity=Freelancer(**freelancer))

    @classmethod
    @validate_arguments
    async def get_freelancer_by_email(cls, email: str) -> EntityResp:
        cls.logger.debug(f"retrieveing freelancer by email {email}")

        freelancer = await db.get_freelancer_by_email(email)
        if not freelancer:
            return err.email_not_found(email, cls.logger)

        return EntityResp(entity=Freelancer(**freelancer))

    @classmethod
    @validate_arguments
    async def add_freelancer(cls, new_freelancer: Freelancer) -> MsgResp:
        cls.logger.debug(f"adding freelancer {new_freelancer.dict()}")

        new_freelancer.password = security.generate_password_hash(new_freelancer.password)

        if await db.get_freelancer_by_email(new_freelancer.email):
            return err.already_exist_freelancer_with_email(new_freelancer.email)

        res = await db.add_freelancer(new_freelancer)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(
                new_freelancer.dict(exclude_none=True), op="insert", logger=cls.logger
            )

        return MsgResp(msg=f"freelancer {new_freelancer.email} saved to db")

    @classmethod
    @validate_arguments
    async def update_freelancer(cls, email: str, freelancer: FreelancerUpdate) -> MsgResp:
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

        return MsgResp(msg=f"freelancer {email} updated in db")

    @classmethod
    @validate_arguments
    async def delete_freelancer(cls, email: str) -> MsgResp:
        cls.logger.debug(f"deleting freelancer {email}")

        if not await db.get_freelancer_by_email(email):
            return err.email_not_found(email, cls.logger)

        res = await db.delete_freelancer(email)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(
                {"freelancer_email": email}, op="delete", logger=cls.logger
            )

        return MsgResp(msg=f"freelancer {email} deleted from db")

    @classmethod
    @validate_arguments
    async def get_nearest(cls, filter: NearestFilterReq) -> EntityResp:

        available_freelancers = await db.find_nearest_freelancers(filter)
        
        cls.logger.debug(f"available nearest freelancers {available_freelancers}")

        return EntityResp(entity=available_freelancers)
