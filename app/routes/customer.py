from fastapi import APIRouter, status

from app.services.customer import CrudCustomer
from app.services.job import CrudJob
from skip_common_lib.schemas import customer as customer_schema
from skip_common_lib.schemas import job as job_schema
from skip_common_lib.schemas import response as resp_schema


router = APIRouter(prefix="/customer")


@router.get("/{email}", response_model=resp_schema.EntityResponse, status_code=status.HTTP_200_OK)
async def get_customer(email: str):
    """Get customer from database by email.

    Args:
        email (str): Email of required customer.

    Returns:
        resp_schema.EntityResponse
    """
    return await CrudCustomer.get_customer_by_email(email)


@router.post(response_model=resp_schema.MsgResponse, status_code=status.HTTP_201_CREATED)
async def add_customer(customer: customer_schema.Customer):
    """Add customer to database.

    Args:
        customer (customer_schema.Customer): Customer to add.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudCustomer.add_customer(customer)


@router.patch("/{email}", response_model=resp_schema.MsgResponse, status_code=status.HTTP_200_OK)
async def update_customer(email: str, customer: customer_schema.CustomerUpdate):
    """Update customer in database by current customer's email (before update).

    Args:
        email (str): Current email of the customer wants to update.
        customer (customer_schema.CustomerUpdate): Customer to update.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudCustomer.update_customer(email, customer)


@router.delete("/{email}", response_model=resp_schema.MsgResponse, status_code=status.HTTP_200_OK)
async def delete_customer(email: str):
    """Delete customer from database by email.

    Args:
        email (str): Email of customer wants to delete.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudCustomer.delete_customer(email)


@router.post("/job", response_model=resp_schema.MsgResponse, status_code=status.HTTP_201_CREATED)
async def post_job(job: job_schema.Job):
    """Post new incoming job to abailable and relevane freelancer.
    Actually, insert the new job the a 'new-job' queue.

    Args:
        job (job_schema.Job): Job to post.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudJob.post_job(job)
