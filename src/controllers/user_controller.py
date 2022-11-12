from flask import Blueprint, request, abort, jsonify, make_response
from init import db, bcrypt
from models.user import User, UserSchema
from models.address import Address, AddressSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta


user_bp = Blueprint('user', __name__, url_prefix='/user')

# Authorization Functions


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
            user_name=request.json['user_name'],
            email=request.json['email'],
            password=bcrypt.generate_password_hash(
                request.json['password']).decode('utf8')
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'Error': 'Email address registered, please login.'}, 409


# Log in and authorize user
@user_bp.route('/login/', methods=['POST'])
def login():
    user = User.query.filter_by(
        email=request.json['email']).first()
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(days=30))
        return {'token': access_token}, 200
    else:
        return {'error': 'Invalid login details, please try again.'}, 401

# Update user details


@user_bp.route('/update/', methods=['PUT', 'PATCH'])
@jwt_required()
def update():

    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    data = UserSchema().load(request.json, partial=True)

    if user:
        user.user_name = data.get('user_name') or user.user_name
        user.email = data.get('email') or user.email
        if data.get('password'):
            user.password = bcrypt.generate_password_hash(
                data.get('password')).decode('utf8') or user.password

    db.session.commit()
    return UserSchema(exclude=['password']).dump(user), 200

# Update user by id if user is admin


@user_bp.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(id):
    admin_auth()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)

    data = UserSchema().load(request.json, partial=True)

    if user:
        user.user_name = data.get('user_name') or user.user_name
        user.email = data.get('email') or user.email
        if data.get('password'):
            user.password = bcrypt.generate_password_hash(
                data.get('password')).decode('utf8') or user.password

    db.session.commit()
    return UserSchema(exclude=['password']).dump(user), 200

# Delete User by id if user is admin


@user_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    admin_auth()
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': f'User {user.user_name} has been deleted successfully.'}, 202
    else:
        return {'error': 'User does not exist'}, 401


# Route to add address to user profile
@user_bp.route('/add_address/', methods=['POST'])
@jwt_required()
def add_address():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        address = Address(
        first_name = request.json['first_name'],
        last_name = request.json['last_name'],
        street_number = request.json['street_number'],
        street = request.json['street'],
        city = request.json['city'],
        state = request.json['state'],
        post_code = request.json['post_code'],
        country = request.json['country'],
        phone = request.json['phone'],
        user_id = user_id
        )

        db.session.add(address)
        db.session.commit()
        return AddressSchema().dump(address), 200
    else:
        return {'error': 'Invalid token'}, 401


# Route to view all addresses for a user
@user_bp.route('/view_addresses/', methods=['GET'])
@jwt_required()
def view_addresses():
    user_id = get_jwt_identity()
    stmt = db.select(Address).filter_by(user_id=user_id)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses), 200
