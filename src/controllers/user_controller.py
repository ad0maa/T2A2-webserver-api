from flask import Blueprint, request
# from main import app
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/users/', methods=['GET'])
def get_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


@user_bp.route('/register/', methods=['POST'])
def register():
    user = User(
    user_name = request.json['user_name'],
    email_address = request.json['email_address'],
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf8')
    )

    db.session.add(user)
    db.session.commit()

    return UserSchema(exclude=['password']).dump(user), 201