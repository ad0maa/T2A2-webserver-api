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
    # address_id = db.Column("Address", back_populates="users")
    # address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable = True)

    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=True)

    # address = db.relationship('Address', back_populates='users', cascade='all, delete')
    # need to add address_id as foreign key

class UserSchema(ma.Schema):

    class Meta:
        fields = ('id', 'user_name', 'email_address', 'password','admin')