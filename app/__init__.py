import os

from flask import Flask
from skip_common_lib.config import BaseConfig


def create_app(app_config: BaseConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config)

    with app.app_context():
        from skip_common_lib.utils import custom_encoders
        from app.services import scheduled_tasks

        from skip_common_lib.database import mongo
        mongo.init_app(app)

        # init flask-extensions
        from skip_common_lib.extensions import jwt, scheduler
        jwt.init_app(app)
        scheduler.init_app(app)

        from app.routes import login, customer, freelancer
        app.register_blueprint(login.login_bp)
        app.register_blueprint(customer.customer_crud_bp)
        app.register_blueprint(freelancer.freelancer_crud_bp)

        # preventing from starting the scheduler twice (Werkzug launches two threads in order to reload the flask application on changes made)
        if app.config["ENV"] == "development" and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            scheduler.start()

        return app
