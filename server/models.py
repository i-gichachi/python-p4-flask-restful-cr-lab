from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    serialize_rules = ('-id',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)  
    price = db.Column(db.Float, nullable=False)

    serialize_rules = ('-id',)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price
        }