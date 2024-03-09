from . import db
from sqlalchemy import ForeignKey, Column, Integer, String, BLOB, Float, Text
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.mysql import LONGTEXT


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name = Column(String(30))
    description = Column(String(500))
    image = Column(LONGTEXT)
    energy_100g = Column(Float)
    proteins_100g = Column(Float)
    carbohydrates_100g = Column(Float)
    sugars_100g = Column(Float)
    fat_100g = Column(Float)
    saturated_fat_100g = Column(Float)
    fiber_100g = Column(Float)
    salt_100g = Column(Float)
    health_score = Column(Float)

    @classmethod
    def create(
            cls, user_id,
            name, description,
            image, energy_100g,
            proteins_100g, carbohydrates_100g, sugars_100g, fat_100g, saturated_fat_100g, fiber_100g, salt_100g,
            health_score
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
            health_score=health_score
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
