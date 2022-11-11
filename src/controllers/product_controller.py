from flask import Blueprint, request
from init import db
from models.product import Product, ProductSchema
from models.review import Review, ReviewSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import and_


product_bp = Blueprint('product', __name__, url_prefix='/product')


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


#Search for products by length
@product_bp.route('/length/<string:query>/<int:length>', methods=['GET'])
def search_length(query,length):
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
def search_volume(query,volume):
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
def search_price(query,price):
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
    stmt = db.select(Product).filter_by(id=product_id)
    card = db.session.scalar(stmt)

    if card:
        review = Review(
            user_id = get_jwt_identity(),
            product_id = product_id,
            title = request.json['title'],
            comment = request.json['comment'],
            rating = request.json['rating']
        )

        db.session.add(review)
        db.session.commit()

        return ReviewSchema().dump(review), 201
    else:
        return {'error': f'No product found with id {id}'}, 404



# @review_bp.route('/<int:product_id>/', methods=['POST'])
# def create():
#     review = Review(
#     user_id = request.json['user_id'],
#     product_id = request.json['product_id'],
#     rating = request.json['rating'],
#     review = request.json['review']
#     )

#     db.session.add(review)
#     db.session.commit()

#     return ReviewSchema().dump(review), 201