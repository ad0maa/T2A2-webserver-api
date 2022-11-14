from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import OneOf, Length
from marshmallow.exceptions import ValidationError
from sqlalchemy import ForeignKey
from datetime import datetime

# Validation for Review Rating
VALID_RATINGS = (0, 1, 2, 3, 4, 5)

# Review Model


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user = db.relationship(
        'User', back_populates='reviews')
    product = db.relationship(
        'Product', back_populates='reviews')

# Review Schema


class ReviewSchema(ma.Schema):

    title = fields.String(required=True, validate=Length(
        min=1, error="Title cannot be blank"))
    rating = fields.Integer(validate=OneOf(
        VALID_RATINGS), error="Rating must be between 0 and 5")
    date = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    @validates('rating')
    def validate_rating(self, value):
        if value not in VALID_RATINGS:
            raise ValidationError('Invalid rating')

    class Meta:
        fields = ('id', 'user_id', 'product_id', 'title',
                  'date', 'comment', 'rating', 'user', 'product')
        ordered = True

    user = fields.Nested('UserSchema', only=['user_name'])
    product = fields.Nested('ProductSchema', only=(
        'name', 'price'))
