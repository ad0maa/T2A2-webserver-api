from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema
from models.review import Review, ReviewSchema
from controllers.user_controller import admin_auth
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_


product_bp = Blueprint('product', __name__, url_prefix='/products')

# Returns all products in database


@product_bp.route('/all', methods=['GET'])
def view_all():
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)

# Returns product by id


@product_bp.route('/<int:id>', methods=['GET'])
def search_id(id):
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product)
    else:
        return {'error': f'No item found with id {id}'}, 404


# Route to add new product to database if user is admin
@product_bp.route('/add', methods=['POST'])
@jwt_required()
def add_product():
    admin_auth()
    data = ProductSchema().load(request.json)
    product = Product(
        name=request.json['name'],
        description=request.json['description'],
        length=request.json['length'],
        volume=request.json['volume'],
        price=request.json['price'],
    )

    db.session.add(product)
    db.session.commit()

    return ProductSchema().dump(product), 200

# Route to update product in database if user is admin
@product_bp.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(id):
    admin_auth()
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    data = ProductSchema().load(request.json)
    
    if product:
        product.name = data.get('name') or product.name
        product.description = data.get('description') or product.description
        product.length = data.get('length') or product.length
        product.volume = data.get('volume') or product.volume
        product.price = data.get('price') or product.price

        db.session.commit()


        return ProductSchema().dump(product), 200
    else:
        return {'error': f'No item found with id {id}'}, 404

# Route to delete product from database if user is admin
@product_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    admin_auth()
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': f'Product {product.id} - {product.name} has been deleted successfully.'}, 202
    else:
        return {'error': f'No item found with id {id}'}, 404


# Search for products by length
@product_bp.route('/length/<string:query>/<int:length>', methods=['GET'])
def search_length(query, length):
    if query == 'min':
        stmt = db.select(Product).filter(and_(Product.length >= length))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'max':
        stmt = db.select(Product).filter(and_(Product.length <= length))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'exact':
        stmt = db.select(Product).filter(and_(Product.length == length))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)


# Search for products by volume
@product_bp.route('/volume/<string:query>/<int:volume>', methods=['GET'])
def search_volume(query, volume):
    if query == 'min':
        stmt = db.select(Product).filter(and_(Product.volume >= volume))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'max':
        stmt = db.select(Product).filter(and_(Product.volume <= volume))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'exact':
        stmt = db.select(Product).filter(and_(Product.volume == volume))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)


# Search for products by price
@product_bp.route('/price/<string:query>/<int:price>', methods=['GET'])
def search_price(query, price):
    if query == 'min':
        stmt = db.select(Product).filter(and_(Product.price >= price))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'max':
        stmt = db.select(Product).filter(and_(Product.price <= price))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)

    elif query == 'exact':
        stmt = db.select(Product).filter(and_(Product.price == price))
        product = db.session.scalars(stmt)
        return ProductSchema(many=True).dump(product)


# Reviews

@product_bp.route('/<int:product_id>/review', methods=['POST'])
@jwt_required()
def create(product_id):
    data = ReviewSchema().load(request.json)
    stmt = db.select(Product).filter_by(id=product_id)
    card = db.session.scalar(stmt)

    if card:
        review = Review(
            user_id=get_jwt_identity(),
            product_id=product_id,
            title=request.json['title'],
            comment=request.json['comment'],
            rating=request.json['rating']
        )

        db.session.add(review)
        db.session.commit()

        return ReviewSchema().dump(review), 201
    else:
        return {'error': f'No product found with id {id}'}, 404


# Returns all reviews for a product
@product_bp.route('/<int:product_id>/review', methods=['GET'])
def view_reviews(product_id):
    stmt = db.select(Review).filter_by(product_id=product_id)
    reviews = db.session.scalars(stmt)
    return ReviewSchema(many=True).dump(reviews)

# Delete a review as admin

@product_bp.route('/<int:product_id>/review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(product_id, review_id):
    admin_auth()
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {'message': f'Review {review.id} has been deleted successfully.'}, 202
    else:
        return {'error': f'No review found with id {id}'}, 404