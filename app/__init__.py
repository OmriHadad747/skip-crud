import pydantic as pyd
import logging

from fastapi import FastAPI
from logging.config import dictConfig


def create_app(settings: pyd.BaseSettings) -> FastAPI:
    app = FastAPI()

    # init settings
    from skip_common_lib.settings import app_settings
    app_settings.init(settings)

    # init logging configuration
    from app.logging import LogConfig
    dictConfig(LogConfig().dict())    

    # init tasks
    from app import sched_tasks
    app.include_router(sched_tasks.scheduler)

    # init routes
    from app.routes import login, customer, freelancer
    app.include_router(login.api)
    app.include_router(customer.api)
    app.include_router(freelancer.api)

    return app
