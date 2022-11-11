from flask import Flask
from init import db, ma, jwt, bcrypt
from controllers.cli_commands import db_commands
from controllers.user_controller import user_bp
from controllers.product_controller import product_bp
from marshmallow.exceptions import ValidationError
import os


def create_app():
    app = Flask(__name__)

    # ERROR HANDLERS to return JSON responses instead of HTML
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(405)
    def not_allowed(err):
        return {'error': str(err)}, 405

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action.'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error', f'The field {err} is required.'}, 400

    @app.errorhandler(ValidationError)
    def key_error(err):
        return {'error': err.messages}, 400

    # Test route

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    # Config for JWT and SQLAlchemy Database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JSON_SORT_KEYS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Initialize SQLAlchemy, Marshmallow, JWT and Bcrypt
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    # app.register_blueprint(review_bp)

    return app
