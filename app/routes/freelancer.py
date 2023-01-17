from fastapi import status

from app.routes import freelancer_router as api
from app.services.freelancer import CrudFreelancer
from app.schemas.freelancer import Freelancer, FreelancerUpdate
from app.schemas.response import EntityResp, MsgResp
from app.schemas.request import NearestFilterReq


@api.get("/freelancer/{email}", response_model=EntityResp, status_code=status.HTTP_200_OK)
async def get_freelancer(email: str):
    """Get freelancer from database by email.

    Args:
        email (str): Email of required freelancer.

    Returns:
        EntityResponse
    """
    return await CrudFreelancer.get_freelancer_by_email(email)


@api.post("/freelancer", response_model=MsgResp, status_code=status.HTTP_201_CREATED)
async def add_freelancer(freelancer: Freelancer):
    """Add freelancer to database.

    Args:
        freelancer (Customer): Customer to add.

    Returns:
        MsgResp
    """
    return await CrudFreelancer.add_freelancer(freelancer)


@api.patch("/freelancer/{email}", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def update_freelancer(email: str, freelancer: FreelancerUpdate):
    """Update freelancer in database by current freelancer's email (before update).

    Args:
        email (str): Current email of the freelancer wants to update.
        freelancer (FreelancerUpdate): Customer to update.

    Returns:
        MsgResp
    """
    return await CrudFreelancer.update_freelancer(email, freelancer)


@api.delete("/freelancer/{email}", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def delete_freelancer(email: str):
    """Delete freelancer from database by email.

    Args:
        email (str): Email of freelancer wants to delete.

    Returns:
        MsgResp
    """
    return await CrudFreelancer.delete_freelancer(email)


@api.post("/freelancer/nearest", response_model=EntityResp, status_code=status.HTTP_200_OK)
async def get_nearest_freelancers(filter: NearestFilterReq):
    """Return a list of available freelancer.

    Args:
        filter (NearestFilterReq): Filter to freelancers searching.

    Returns:
        EntityResp
    """
    return await CrudFreelancer.get_nearest(filter)
