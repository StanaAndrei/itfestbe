from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped


class Fav(db.Model):
    __tablename__ = 'favs'
    id = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    prod_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product = db.relationship('Product', backref='fav', lazy='joined')

    @classmethod
    def create(cls, user_id, prod_id):
        new_fav = cls(user_id=user_id, prod_id=prod_id)
        db.session.add(new_fav)
        db.session.commit()
        return new_fav

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
