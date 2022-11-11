from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String,  nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)


    reviews = db.relationship('Review', back_populates='user')

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'admin')
        ordered = True


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    post_code = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)


class AddressSchema(ma.Schema):

    class Meta:
        fields = ('id', 'user', 'first_name', 'last_name', 'street_number',
                  'street', 'city', 'state', 'post_code', 'country', 'phone_number')
        ordered = True
