import os

from flask import Flask

from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()

    return app
