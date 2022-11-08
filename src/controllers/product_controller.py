from flask import Blueprint
from init import db
from models.product import Product, ProductSchema
from sqlalchemy import and_

product_bp = Blueprint('product', __name__, url_prefix='/product')

@product_bp.route('/all', methods=['GET'])
def view_all():

    # stmt = db.select(Product)
    stmt = db.select(Product)
    products = db.session.scalars(stmt)
    return ProductSchema(many=True).dump(products)


@product_bp.route('/<int:id>', methods=['GET'])
def search_id(id):
    stmt = db.select(Product).filter_by(id=id)
    product = db.session.scalar(stmt)
    if product:
        return ProductSchema().dump(product)
    else:
        return {'error': f'No item found with id {id}'}, 404



#Search for products by minimum length - returns all surfboards that are longer than length provided by client
# @product_bp.route('/length/<int:length>', methods=['GET'])
# def search_length(length):
#     stmt = db.select(Product).filter(and_(Product.length >= length))
#     product = db.session.scalars(stmt)
#     if product:
#         return ProductSchema(many=True).dump(product)
#     else:
#         return {'error': f'No item found with id {id}'}, 404


#Search for products by minimum length - returns all surfboards that are longer than length provided by client
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



    # stmt = db.select(Product).filter_by(Product.length)
    # product = db.session.scalars(stmt)
    # if product:
    #     return ProductSchema(many=True).dump(product)
    # else:
    #     return {'error': f'No item found with id {id}'}, 404