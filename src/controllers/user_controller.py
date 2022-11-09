from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/view_all/', methods=['GET'])
def view_all():
    # add authorization
    auth = request.headers.get('Authorization')
    if auth:
        auth = auth.replace('Bearer ', '')
        user_id = get_jwt_identity()
        if user_id:
            stmt = db.select(User)
            users = db.session.scalars(stmt)
            return UserSchema(many=True).dump(users)
        else:
            return {'error': 'Invalid token'}, 401

    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)


# register a user
@user_bp.route('/register/', methods=['POST'])
def register():
    try:
        user = User(
            name=request.json['name'],
            email_address=request.json['email_address'],
            password=bcrypt.generate_password_hash(
                request.json['password']).decode('utf8')
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude='password').dump(user), 201

    except IntegrityError:
        
            return {'Error': 'Email address registered, please login.'}, 409


# log in and authorize user
@user_bp.route('/login/', methods=['POST'])
def login():
    user = User.query.filter_by(
        email_address=request.json['email_address']).first()
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(identity=user.id)
        return {'token': access_token}, 200
    else:
        return {'error': 'Invalid credentials'}, 401
