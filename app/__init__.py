# app/__init__.py

from flask import Flask
from config import config_by_name
from .routers.questions import questions_bp
from .routers.responses import responses_bp
from .routers.users import users_bp
from .routers.categories import categories_bp
from app.models import db
from flask_migrate import Migrate
import os


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    app.register_blueprint(questions_bp)
    app.register_blueprint(responses_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    return app