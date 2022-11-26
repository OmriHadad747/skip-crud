import pydantic as pyd

from fastapi import FastAPI


def create_app(settings: pyd.BaseSettings) -> FastAPI:
    app = FastAPI()

    from skip_common_lib.settings import app_settings

    app_settings.init(settings)

    return app
