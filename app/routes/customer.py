from fastapi import status

from app.routes import customer_router as api
from app.schemas.customer import Customer, CustomerUpdate
from app.schemas.response import MsgResp, EntityResp
from app.services.customer import CrudCustomer


@api.get(
    "/customer/{email}",
    response_model=EntityResp,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": MsgResp}},
)
async def get_customer(email: str):
    return await CrudCustomer.get_customer_by_email(email)


@api.post(
    "/customer",
    response_model=MsgResp,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": MsgResp},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MsgResp},
    },
)
async def add_customer(customer: Customer):
    return await CrudCustomer.add_customer(customer)


@api.patch(
    "/customer/{email}",
    response_model=MsgResp,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": MsgResp},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MsgResp},
    },
)
async def update_customer(email: str, customer: CustomerUpdate):
    return await CrudCustomer.update_customer(email, customer)


@api.delete(
    "/customer/{email}",
    response_model=MsgResp,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": MsgResp},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MsgResp},
    },
)
async def delete_customer(email: str):
    return await CrudCustomer.delete_customer(email)
