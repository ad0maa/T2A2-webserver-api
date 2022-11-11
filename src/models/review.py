from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf
from sqlalchemy import ForeignKey
from datetime import datetime


VALID_RATINGS = (0, 1, 2, 3, 4, 5)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=True, default=datetime.now)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship(
        'User', back_populates='reviews')
    product = db.relationship(
        'Product', back_populates='reviews')


class ReviewSchema(ma.Schema):

    rating = fields.Integer(validate= OneOf(VALID_RATINGS))
    date = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        fields = ('id', 'user_id', 'product_id', 'title',
                  'date', 'comment', 'rating', 'user')
        ordered = True

    user = fields.Nested('UserSchema', only=('name',))
    product = fields.Nested('ProductSchema', only=(
        'id', 'name', 'description', 'price', 'image_url', 'category_id'))