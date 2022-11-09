from flask import Flask
from init import db, ma, jwt, bcrypt
from controllers.cli_commands import db_commands
from controllers.user_controller import user_bp
from controllers.product_controller import product_bp
from controllers.review_controller import review_bp
import os



def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello, World!"


    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config ['JSON_SORT_KEYS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(db_commands)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(review_bp)

    return app