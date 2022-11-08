from init import db, ma
from marshmallow import fields
from sqlalchemy import ForeignKey

class Review(db.Model):



    user = db.relationship('User', back_populates='reviews')