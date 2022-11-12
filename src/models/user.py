from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey
from models.address import Address, AddressSchema


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100),  nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user', cascade="all, delete")
    address = db.relationship('Address', back_populates='user')

class UserSchema(ma.Schema):

    # address = fields.Nested('AddressSchema', only=('id', 'first_name', 'last_name', 'street_number', 'street', 'city', 'state', 'post_code', 'country', 'phone', 'user_id', 'user'))

    address = fields.Nested('AddressSchema', only=('id', 'first_name', 'last_name', 'street_number', 'street', 'city', 'state', 'post_code', 'country', 'phone', 'user_id', 'user'))

    class Meta:
        fields = ('id', 'user_name', 'email', 'password', 'admin', 'address')
        ordered = True
