from . import db


class User(db.Model):
    __tablename__: str = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    @classmethod
    def create_user(cls, email, password, username):
        new_user = cls(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def as_dict(self):
        excluded_attributes = ["password"]  # Add any other attributes you want to exclude
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in excluded_attributes}