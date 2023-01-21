import logging

from pydantic import validate_arguments
from werkzeug import security

from app.errors import Errors as err
from app.schemas.customer import Customer, CustomerUpdate
from app.schemas.response import MsgResp, EntityResp
from app.database.customer import CustomerDB as db


class CrudCustomer:
    logger = logging.getLogger("skip-crud-service")

    @classmethod
    @validate_arguments
    async def get_customer_by_id(cls, id: str) -> EntityResp:
        cls.logger.debug(f"retrieveing customer by id {id}")

        customer = await db.get_customer_by_id(id)
        if not customer:
            return err.id_not_found(id)

        return EntityResp(output=dict(customer))

    @classmethod
    @validate_arguments
    async def get_customer_by_email(cls, email: str) -> EntityResp:
        cls.logger.debug(f"retrieveing customer by email {email}")

        customer = await db.get_customer_by_email(email)
        if not customer:
            return err.email_not_found(email)

        return EntityResp(output=customer)

    @classmethod
    @validate_arguments
    async def add_customer(cls, new_customer: Customer) -> MsgResp:
        cls.logger.debug(f"adding customer {new_customer.dict()}")

        new_customer.password = security.generate_password_hash(new_customer.password)

        if await db.get_customer_by_email(new_customer.email):
            return err.already_exist_customer_with_email(new_customer.email, cls.logger)

        res = await db.add_customer(new_customer)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(new_customer.dict(exclude_none=True), op="insert")

        return MsgResp(msg=f"customer {new_customer.email} saved to db")

    @classmethod
    @validate_arguments
    async def update_customer(cls, email: str, customer: CustomerUpdate) -> MsgResp:
        cls.logger.debug(
            f"udpating customer {email} with fields {customer.dict(exclude_none=True)}"
        )

        if customer.password:
            customer.password = security.generate_password_hash(customer.password)

        if not await db.get_customer_by_email(email):
            return err.email_not_found(email, cls.logger)

        res = await db.update_customer(email, customer)
        if not res.acknowledged:
            return err.db_op_not_acknowledged(customer.dict(exclude_none=True), op="update")

        return MsgResp(msg=f"customer {email} updated in db")

    @classmethod
    @validate_arguments
    async def delete_customer(cls, email: str) -> MsgResp:
        cls.logger.debug(f"deleting customer {email}")

        if not await db.get_customer_by_email(email):
            return err.email_not_found(email, cls.logger)

        res = await db.delete_customer(email)
        if not res.acknowledged:
            return err.db_op_not_acknowledged({"customer_email": email}, op="delete")

        return MsgResp(msg=f"customer {email} deleted from db")
