import os

from app import config
from flask import Flask


def create_app(app_config: config.BaseConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config)

    with app.app_context():
        from app.utils import custom_json_encoder
        from app.services import scheduled_tasks

        # init flask-extensions
        from app import extensions

        extensions.jwt.init_app(app)
        extensions.scheduler.init_app(app)

        from skip_db_lib.database import mongo
        mongo.init_app(app)

        from app.routes import login, customer, freelancer
        app.register_blueprint(customer.customer_crud_bp)
        app.register_blueprint(freelancer.freelancer_crud_bp)
        app.register_blueprint(login.login_bp)

        # preventing from starting the scheduler twice (Werkzug launches two threads in order to reload the flask application on changes made)
        if app.config["ENV"] == "development" and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
            extensions.scheduler.start()

        return app
