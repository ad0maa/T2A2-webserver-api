from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email_address = db.Column(db.String,  nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)   
    admin = db.Column(db.Boolean, default=False)
    # need to add address_id as foreign key

