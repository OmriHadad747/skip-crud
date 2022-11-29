import pydantic as pyd

from fastapi import FastAPI


def create_app(settings: pyd.BaseSettings) -> FastAPI:
    app = FastAPI()

    from skip_common_lib.settings import app_settings
    app_settings.init(settings)

    from app import routes
    app.include_router(routes.login_router)
    app.include_router(routes.customer_router)
    app.include_router(routes.freelancer_router)

    return app
