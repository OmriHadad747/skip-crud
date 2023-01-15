from typing import Any
from fastapi import status

from app.schemas.response import MsgResp


class Errors:
    @classmethod
    def db_op_not_acknowledged(cls, obj: Any, op: str):
        return MsgResp(
            msg=f"internal server error : db operation {op.upper()} on {obj} doesn't acknowledged"
        ).json_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def already_exist_customer_with_email(cls, email: str):
        return MsgResp(msg=f"already exist customer with mail: {email}").json_response(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    @classmethod
    def id_not_found(cls, id: str):
        return MsgResp(msg=f"{id} not found").json_response(status_code=status.HTTP_404_NOT_FOUND)

    @classmethod
    def email_not_found(cls, email: str):
        return MsgResp(msg=f"{email} not found").json_response(
            status_code=status.HTTP_404_NOT_FOUND
        )
