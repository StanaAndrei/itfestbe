from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    with app.app_context():
        db.init_app(app)
        from .user import User
        from .product import Product
        from .fav import Fav
        db.create_all()
