import pydantic as pyd

from fastapi import FastAPI
from logging.config import dictConfig


def create_app(settings: pyd.BaseSettings) -> FastAPI:
    app = FastAPI()

    # init settings
    from app.settings import app_settings

    app_settings.init(settings)

    # init logging
    from skip_common_lib.logging import LogConfig

    dictConfig(LogConfig().dict())

    # init tasks
    from app import tasks

    app.include_router(tasks.scheduler)

    # init routes
    from app.routes import login, customer, freelancer, job

    app.include_router(login.api, tags=["Login"])
    app.include_router(customer.api, tags=["Customer"])
    app.include_router(freelancer.api, tags=["Freelancer"])
    app.include_router(job.api, tags=["Job"])

    return app
