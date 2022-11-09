from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    length = db.Column(db.Integer)   
    volume = db.Column(db.Integer)
    price = db.Column(db.Numeric(12,2))

    reviews = db.relationship('Review', back_populates='product', cascade="all, delete")
    

class ProductSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'length','volume', 'price')
        ordered = True