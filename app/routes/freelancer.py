from fastapi import status

from app.routes import freelancer_router as api
from app.services.freelancer import CrudFreelancer
from app.schemas.freelancer import Freelancer, FreelancerUpdate
from app.schemas.response import EntityResp, MsgResp
from app.schemas.request import NearestFilterReq


@api.get("/freelancer/{email}", response_model=EntityResp, status_code=status.HTTP_200_OK)
async def get_freelancer(email: str):
    return await CrudFreelancer.get_freelancer_by_email(email)


@api.post("/freelancer", response_model=MsgResp, status_code=status.HTTP_201_CREATED)
async def add_freelancer(freelancer: Freelancer):
    return await CrudFreelancer.add_freelancer(freelancer)


@api.patch("/freelancer/{email}", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def update_freelancer(email: str, freelancer: FreelancerUpdate):
    return await CrudFreelancer.update_freelancer(email, freelancer)


@api.delete("/freelancer/{email}", response_model=MsgResp, status_code=status.HTTP_200_OK)
async def delete_freelancer(email: str):
    return await CrudFreelancer.delete_freelancer(email)


@api.post("/freelancer/nearest", response_model=EntityResp, status_code=status.HTTP_200_OK)
async def get_nearest_freelancers(filter: NearestFilterReq):
    return await CrudFreelancer.get_nearest(filter)
