from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey
from datetime import datetime


VALID_RATINGS = (0, 1, 2, 3, 4, 5)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable = False)
    title  = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    comments = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='reviews', cascade="all, delete")
    product = db.relationship('Product', back_populates='reviews', cascade="all, delete")


class ReviewSchema(ma.Schema):


    class Meta:
        fields = ('id', 'user_id', 'product_id', 'title', 'date', 'comments', 'rating', 'user')
        ordered = True

    user = fields.Nested('UserSchema', only=('user_name', 'email_address', 'admin'))
    product = fields.Nested('ProductSchema', only=('id', 'name', 'description', 'price', 'image_url', 'category_id'))

    # user = fields.Nested('UserSchema', only=('user_name'))

    # class Meta:
    #     fields = ('id', 'user_id', 'product_id', 'title','date', 'comments', 'rating', 'user')
    #     ordered = True