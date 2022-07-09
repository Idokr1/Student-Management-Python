from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
db = SQLAlchemy()

from flask_bcrypt import Bcrypt
flask_bcrypt = Bcrypt()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app