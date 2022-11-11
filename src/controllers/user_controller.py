from flask import Blueprint, request, abort, jsonify, make_response
from init import db, bcrypt
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta


user_bp = Blueprint('user', __name__, url_prefix='/user')

# Authorization Functions


def user_auth():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

def admin_auth():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    if not user.admin:
        abort(make_response(
            jsonify(error='You are not authorized to perform this action'), 403))


# Route that allows admin to view all users


@user_bp.route('/view_all/', methods=['GET'])
@jwt_required()
def view_all():
    admin_auth()
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

# Register a new user and check that user does not already exist in the database


@user_bp.route('/register/', methods=['POST'])
def register():
    try:
        user = User(
            name=request.json['name'],
            email=request.json['email'],
            password=bcrypt.generate_password_hash(
                request.json['password']).decode('utf8')
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'Error': 'Email address registered, please login.'}, 409


# log in and authorize user
@user_bp.route('/login/', methods=['POST'])
def login():
    user = User.query.filter_by(
        email=request.json['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(
            identity=user.id,  expires_delta=timedelta(days=1))
        return {'token': access_token}, 200
    else:
        return {'error': 'Invalid login details, please try again.'}, 401

# update user details


@user_bp.route('/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update():

    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    data = UserSchema().load(request.json, partial=True)

    if user:
        user.name = data.get('name') or user.name
        user.email = data.get('email') or user.email
        if data.get('password'):
            user.password = bcrypt.generate_password_hash(
            data.get('password')).decode('utf8') or user.password

    db.session.commit()
    return UserSchema(exclude=['password']).dump(user), 200

# delete user


@user_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    admin_auth()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.name} has been deleted successfully.'}, 202
    else:
        return {'error': 'User does not exist'}, 401


# create route to add address to user profile
@user_bp.route('/add_address/', methods=['POST'])
@jwt_required()
def add_address():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        user.address = request.json['address']
        user.city = request.json['city']
        user.state = request.json['state']
        user.zip_code = request.json['zip_code']
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 200
    else:
        return {'error': 'Invalid token'}, 401
