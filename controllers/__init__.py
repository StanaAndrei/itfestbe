import flask.app

from .user import userBP
from .session import sessionBP
from .product import productBP


def initControllers(app: flask.app.Flask):
    app.register_blueprint(userBP)
    app.register_blueprint(sessionBP)
    app.register_blueprint(productBP)