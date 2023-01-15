from fastapi import status

from app.routes import freelancer_router as api
from app.services.freelancer import CrudFreelancer
from app.schemas import freelancer as freelancer_schema
from app.schemas import response as resp_schema


@api.get(
    "/freelancer/{email}", response_model=resp_schema.EntityResp, status_code=status.HTTP_200_OK
)
async def get_freelancer(email: str):
    """Get freelancer from database by email.

    Args:
        email (str): Email of required freelancer.

    Returns:
        resp_schema.EntityResponse
    """
    return await CrudFreelancer.get_freelancer_by_email(email)


@api.post("/freelancer", response_model=resp_schema.MsgResp, status_code=status.HTTP_201_CREATED)
async def add_freelancer(freelancer: freelancer_schema.Freelancer):
    """Add freelancer to database.

    Args:
        freelancer (freelancer_schema.Customer): Customer to add.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudFreelancer.add_freelancer(freelancer)


@api.patch(
    "/freelancer/{email}", response_model=resp_schema.MsgResp, status_code=status.HTTP_200_OK
)
async def update_freelancer(email: str, freelancer: freelancer_schema.FreelancerUpdate):
    """Update freelancer in database by current freelancer's email (before update).

    Args:
        email (str): Current email of the freelancer wants to update.
        freelancer (freelancer_schema.FreelancerUpdate): Customer to update.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudFreelancer.update_freelancer(email, freelancer)


@api.delete(
    "/freelancer/{email}", response_model=resp_schema.MsgResp, status_code=status.HTTP_200_OK
)
async def delete_freelancer(email: str):
    """Delete freelancer from database by email.

    Args:
        email (str): Email of freelancer wants to delete.

    Returns:
        resp_schema.MsgResponse
    """
    return await CrudFreelancer.delete_freelancer(email)
