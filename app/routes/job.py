from fastapi import status

from app.routes import job_router as api
from app.schemas.response import MsgResp, EntityResp
from app.schemas.job import Job, JobUpdate, JobStatusEnum
from app.services.job import CrudJob


@api.get(
    "job/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntityResp,
    responses={status.HTTP_404_NOT_FOUND: {"model": MsgResp}},
)
async def get_job(job_id: str):
    return await CrudJob.get_job_by_id(job_id)


@api.post(
    "/job",
    status_code=status.HTTP_201_CREATED,
    response_model=MsgResp,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MsgResp}},
)
async def add_job(job: Job):
    return await CrudJob.add_job(job)


@api.patch(
    "/job/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=MsgResp,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MsgResp},
        status.HTTP_404_NOT_FOUND: {"model": MsgResp},
    },
)
async def update_job(
    job_id: str,
    job: JobUpdate,
    current_job_status: JobStatusEnum,
    return_with_updated: bool = False,
):
    return await CrudJob.update_job(job_id, job, current_job_status, return_with_updated)
