from flask import Blueprint, request, abort, jsonify, make_response
from init import db, bcrypt
from models.user import User, UserSchema
from models.address import Address, AddressSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta


user_bp = Blueprint('user', __name__, url_prefix='/user')
address_bp = Blueprint('address', __name__, url_prefix='/user/address')

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

        return UserSchema(exclude=['password', 'address']).dump(user), 201

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
        db.session.add(user)
        db.session.commit()
    else:
        return {'error': 'No user found'}, 404

    return UserSchema(exclude=['password']).dump(user), 200

# Delete User by id as Admin


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
@address_bp.route('/new/', methods=['POST'])
@jwt_required()
def new_address():
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
        return {'error': 'Invalid token, please login.'}, 401

# Route to update address as admin by id
@address_bp.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_address(id):
    admin_auth()
    user_id = get_jwt_identity()
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    data = AddressSchema().load(request.json, partial=True)
    if address:
   
        address.user_id = id or address.user_id,
        address.first_name = data.get('first_name') or address.first_name,
        address.last_name = data.get('last_name') or address.last_name,
        address.street_number = data.get('street_number') or address.street_number,
        address.street = data.get('street') or address.street,
        address.city = data.get('city') or address.city,
        address.state = data.get('state') or address.state,
        address.post_code = data.get('post_code') or address.post_code,
        address.country = data.get('country') or address.country,
        address.phone = data.get('phone') or address.phone
        
        db.session.add(address)
        db.session.commit()
        return AddressSchema().dump(address), 200
    else:
        return {'error': 'Invalid token, please login.'}, 401


# Route to view address for a user by id as admin
@address_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def view_address(id):
    admin_auth()
    stmt = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        return AddressSchema().dump(address), 200
    else:
        return {'error': 'No Address for user with that id'}, 401
