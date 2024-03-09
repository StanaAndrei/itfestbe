from . import db
from sqlalchemy import ForeignKey, Column, Integer, String, BLOB, Float, Text
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.mysql import LONGTEXT


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name = Column(String(100))
    description = Column(String(500))
    image = Column(LONGTEXT)
    energy_100g = Column(Float, default=.0)
    proteins_100g = Column(Float, default=.0)
    carbohydrates_100g = Column(Float, default=.0)
    sugars_100g = Column(Float, default=.0)
    fat_100g = Column(Float, default=.0)
    saturated_fat_100g = Column(Float, default=.0)
    fiber_100g = Column(Float, default=.0)
    salt_100g = Column(Float, default=.0)
    health_score = Column(Float, default=.0)
    category = Column(String(20))

    @classmethod
    def create(
            cls, user_id,
            name, description,
            image, energy_100g,
            proteins_100g, carbohydrates_100g, sugars_100g, fat_100g, saturated_fat_100g, fiber_100g, salt_100g,
            category, health_score
    ):
        new_product = cls(
            user_id=user_id,
            name=name,
            description=description,
            image=image,
            energy_100g=energy_100g,
            proteins_100g=proteins_100g,
            carbohydrates_100g=carbohydrates_100g,
            sugars_100g=sugars_100g,
            fat_100g=fat_100g,
            saturated_fat_100g=saturated_fat_100g,
            fiber_100g=fiber_100g,
            salt_100g=salt_100g,
            category=category,
            health_score=health_score
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


