from flask import Blueprint
# from main import app
from init import db
from models.product import Product, ProductSchema

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