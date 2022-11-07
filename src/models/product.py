from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    length = db.Column(db.String)   
    volume = db.Column(db.String)
    price = db.Column(db.Integer)


class ProductSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'length','volume', 'price')