from flask import Blueprint
from init import db
from models.user import User

db_commands = Blueprint('db', __name__)

# CLI Commands

@db_commands.cli.command('create')
def db_create():
    db.create_all()
    print('Tables Created')

@db_commands.cli.command('drop')
def db_drop():
    db.drop_all()
    print('Tables Dropped')

