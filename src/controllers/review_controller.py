from flask import Blueprint, request
from init import db, bcrypt
from models.review import Review, ReviewSchema
from flask_jwt_extended import create_access_token, get_jwt_identity


review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/view_all/', methods=['GET'])
def view_all():
    stmt = db.select(Review)
    reviews = db.session.scalars(stmt)
    return ReviewSchema(many=True).dump(reviews)

@review_bp.route('/create/', methods=['POST'])
def create():
    review = Review(
    user_id = request.json['user_id'],
    product_id = request.json['product_id'],
    rating = request.json['rating'],
    review = request.json['review']
    )

    db.session.add(review)
    db.session.commit()

    return ReviewSchema().dump(review), 201