from flask import Flask
from init import db, ma,jwt
from controllers.cli_commands import db_commands
import os



def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello, World!"


    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(db_commands)

    return app