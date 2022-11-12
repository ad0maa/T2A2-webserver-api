from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey
from models.user import User, UserSchema


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    street_number = db.Column(db.Integer(), nullable=False)
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    post_code = db.Column(db.Integer(), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='address', cascade="all, delete")


class AddressSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=('id', 'user_name', 'email'))

    class Meta:
        fields = ('id', 'user', 'first_name', 'last_name', 'street_number',
                  'street', 'city', 'state', 'post_code', 'country', 'phone', 'user_id', 'user')
        ordered = True