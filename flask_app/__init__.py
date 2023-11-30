from flask import Flask
from flask_app.services.json.custom_encoder import CustomEncoder


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    if config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the config if passed in
        app.config.from_mapping(config)
    _register_blueprints(app)
    return app


def _register_blueprints(app):
    from .blueprints.sensor import sensor_bp
    app.register_blueprint(sensor_bp)
