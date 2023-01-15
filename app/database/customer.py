from typing import Any
from pymongo import collection, results, ASCENDING
from bson import ObjectId

from app.schemas.customer import Customer, CustomerUpdate
from app.database import db, _customers
from skip_common_lib.utils.custom_encoders import codec_options


class CustomerDB:
    location_indexed = False

    @classmethod
    def _get_coll(cls) -> collection.Collection:
        """
        Returns the relevant collection with pointing to a codec opetion.

        Returns:
            collection.Collection: Customer collection
        """
        if not cls.location_indexed:
            db[_customers].create_index([("email", ASCENDING)])
            cls.location_indexed = True

        return db[_customers].with_options(codec_options=codec_options)

    @classmethod
    async def get_customer_by_id(cls, id: str) -> Any | None:
        customer = await cls._get_coll().find_one({"_id": ObjectId(id)})
        return customer

    @classmethod
    async def get_customer_by_email(cls, email: str) -> Any | None:
        customer = await cls._get_coll().find_one({"email": email})
        return customer

    @classmethod
    async def add_customer(cls, customer: Customer) -> results.InsertOneResult:
        result = await cls._get_coll().insert_one(customer.dict())
        return result

    @classmethod
    async def update_customer(cls, email: str, customer: Customer) -> results.UpdateResult:
        result = await cls._get_coll().update_one(
            {"email": email},
            {"$set": customer.dict(exclude_none=True)},
        )
        return result

    @classmethod
    async def delete_customer(cls, email: str) -> results.DeleteResult:
        result = await cls._get_coll().delete_one({"email": email})
        return result
