from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(100),  nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user', cascade="all, delete")
    address = db.relationship('Address', back_populates='user', cascade="all, delete")

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'user_name', 'email', 'password', 'address', 'admin')
        ordered = True

    address = fields.Nested('AddressSchema')

