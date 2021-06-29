from flask import Flask

import application.rest.room
from application.rest import room


def create_app(config_name: str):

    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    app.register_blueprint(application.rest.room.blueprint)

    return app
