from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    length = db.Column(db.Integer, nullable=True)
    volume = db.Column(db.Integer, nullable = True)
    price = db.Column(db.Numeric(12,2), nullable=False)

    reviews = db.relationship('Review', back_populates='product', cascade="all, delete")
    

class ProductSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'length','volume', 'price')
        ordered = True