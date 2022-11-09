from flask import Blueprint
from init import db
from models.product import Product, ProductSchema
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