import logging

from pydantic import validate_arguments
from werkzeug import security

from skip_common_lib.utils.errors import Errors as err
from skip_common_lib.database.customers import CustomerDB as db
from skip_common_lib.schemas import customer as customer_schema
from skip_common_lib.schemas import response as resp_schema


class CrudCustomer:
    logger = logging.getLogger("skip-crud-service")

    @classmethod
    @validate_arguments
    async def get_customer_by_id(cls, id: str):
        cls.logger.debug(f"retrieveing customer by id {id}")

        customer = await db.get_customer_by_id(id)
        if not customer:
            return err.id_not_found(id, cls.logger)

        resp_schema.EntityResponse(
            args=dict(id=id),
            output=customer
        )

    @classmethod
    @validate_arguments
    async def get_customer_by_email(cls, email: str):
        cls.logger.debug(f"retrieveing customer by email {email}")

        customer = await db.get_customer_by_email(email)
        if not customer:
            return err.email_not_found(email, cls.logger)

        resp_schema.EntityResponse(
            args=dict(email=email),
            output=customer
        )

    @classmethod
    @validate_arguments
    async def add_customer(cls, new_customer: customer_schema.Customer):
        cls.logger.debug(f"adding customer {new_customer.dict()}")

        try:
            new_customer.password = security.generate_password_hash(new_customer.password)

            if await db.get_customer_by_email(new_customer.email):
                return err.already_exist_customer_with_email(new_customer.email, cls.logger)

            res = await db.add_customer(new_customer)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(new_customer.dict(exclude_none=True), op="insert", logger=cls.logger)

        except Exception as e:
            # TODO catch more specifiec exceptions
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=new_customer.dict(),
            msg=f"customer {new_customer.email} saved to db"
        )

    @classmethod
    @validate_arguments
    async def update_customer(cls, email: str, customer: customer_schema.CustomerUpdate):
        cls.logger.debug(f"udpating customer {email} with fields {customer.dict(exclude_none=True)}")

        try:
            if customer.password:
                customer.password = security.generate_password_hash(customer.password)

            if not await db.get_customer_by_email(email):
                return err.email_not_found(email, cls.logger)

            res = await db.update_customer(email, customer)
            if not res.acknowledged:
                return err.db_op_not_acknowledged(customer.dict(exclude_none=True), op="update", logger=cls.logger)

        except Exception as e:
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=customer.dict(exclude_none=True),
            msg=f"customer {email} updated in db"
        )

    @classmethod
    @validate_arguments
    async def delete_customer(cls, email: str):
        cls.logger.debug(f"deleting customer {email}")

        try:
            if not await db.get_customer_by_email(email):
                return err.email_not_found(email, cls.logger)

            res = await db.delete_customer(email)
            if not res.acknowledged:
                return err.db_op_not_acknowledged({"customer_email": email}, op="delete", logger=cls.logger)

        except Exception as e:
            return err.general_exception(e, cls.logger)

        return resp_schema.MsgResponse(
            args=dict(email=email),
            msg=f"customer {email} deleted from db"
        )