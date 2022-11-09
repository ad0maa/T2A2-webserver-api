from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    email_address = db.Column(db.String,  nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)   
    admin = db.Column(db.Boolean, default=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable = True)

    address = db.relationship('Address', back_populates='user', cascade="all, delete")
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete")

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'user_name', 'email_address', 'password','admin')

class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    post_code = db.Column(db.Integer, nullable=False) 
    country = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)

    user = db.relationship('User', back_populates='address', cascade="all, delete")

class AddressSchema(ma.Schema):

    class Meta:
        fields = ('id', 'user_id', 'street_number', 'street','city', 'state', 'post_code', 'country', 'phone_number')
        ordered = True
