from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/users/', methods=['GET'])
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)  