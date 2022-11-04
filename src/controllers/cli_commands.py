from flask import Blueprint
from init import db, bcrypt
from models.user import User

db_commands = Blueprint('db', __name__)

# CLI Commands

@db_commands.cli.command('create')
def db_create():
    db.create_all()
    print('Table Creation Successful')

@db_commands.cli.command('drop')
def db_drop():
    db.drop_all()
    print('Table Drop Successful')

@db_commands.cli.command('seed')
def db_seed():

    users = [
        User(
            username = 'Administrator',
            email_address ='admin@spam.com',
            password = bcrypt.generate_password_hash('password').decode('utf8'),
            admin = True
        ),
        User(
            username = 'adam.tunchay',
            email_address = 'adam.tunchay@me.com',
            password= bcrypt.generate_password_hash('123456').decode('utf8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    print('Table Seeding Successful')