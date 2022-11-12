from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.product import Product
from models.review import Review
from models.address import Address
from datetime import date

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
            user_name='Administrator',
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('password').decode('utf8'),
            admin=True
        ),
        User(
            user_name='adam.tunchay',
            email='adam.tunchay@me.com',
            password=bcrypt.generate_password_hash('123456').decode('utf8'),
            # address=addresses[0]
        ),
        User(
            user_name='mick.hughes',
            email='michael.hughes@gmail.com',
            password=bcrypt.generate_password_hash('password').decode('utf8'),
            # address=addresses[0]
        ),
        User(
            user_name='elisa.smith',
            email='elisa.smith@hotmail.com',
            password=bcrypt.generate_password_hash('password').decode('utf8'),
            # address=addresses[0]
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    addresses = [
        Address(
            first_name='John',
            last_name='Doe',
            street_number=20,
            street='Evergreen Terrace',
            city='Torquay',
            state='Victoria',
            post_code=3228,
            country='Australia',
            phone='0421180150',
            user= users[0]
        )
    ]

    db.session.add_all(addresses)
    db.session.commit()

    products = [
        Product(
            name='Rip Curl Mini-mal Surfboard',
            description='Mini-mal longboard designed on the surfcoast, Victoria.',
            length=8,
            volume=64,
            price=750
        ),
        Product(
            name='Christenson Fish Surfboard',
            description='Double foil fins with low cant and toe complimented by the twin pin tail allow this board to reach high speeds and insure hold whenever on the rail.',
            length=5.6,
            volume=32.4,
            price=1399.99
        ),
        Product(
            name='Hayden Shapes Hypto Krypto Surfboard',
            description='The Hypto Krypto is a balance of tradition and modern performance. Suited to the elite level surfer to the everyday surfer, it is often referred to as the ‘one board quiver’ for its versatility across all types of surf conditions – from small 1-3 ft beach breaks, to barrels of up to 8ft.',
            length=6.2,
            volume=43.2,
            price=849.99
        ),
        Product(
            name='The Critical Slide Society Loggerhead PU Longboard Surfboard',
            description='The Logger Head is a wide and incredibly stable surfboard. The long parallel rails create a huge stable platform to stand and walk the board, and the full rounded nose is ideal for riding the nose.',
            length=9.2,
            volume=70,
            price=1295
        ),
        Product(
            name='Pyzel Padillac Step Up Surfboard',
            description='It has a clean, flowing rocker, and a light vee bottom with double concaves to give you speed and sensitivity while still maintaining control in heavy conditions. It comes as a quad, for both speed and maneuverability, and can handle anything the ocean throws at you.',
            length=7,
            volume=45.8,
            price=1399
        ),
        Product(
            name='Catch Surf Odysea Log 7’0 Softboard',
            description='More is better when it comes to having fun and the LOG delivers! In true Odysea form, the LOG has a classic look and feel with mega-float performance so you can shred with ease and style. So whether you\'re a stoked grom learning to surf or a seasoned vet looking to maximize wave count, the Odysea LOG is for you! The LOG is a legit board designed by real surfers in California. Enjoy!',
            length=7,
            volume=72,
            price=699.99
        )
    ]

    db.session.add_all(products)
    db.session.commit()

    reviews = [
        Review(
            user=users[1],
            product=products[0],
            title='Great board',
            rating=5,
            comment='This board is amazing, I love it!',
            date=date.today()
        ),
        Review(
            user=users[0],
            product=products[1],
            title='Not a fan',
            rating=3,
            comment='Volume is a bit small for me, but it\'s a great board.'
        )
    ]

    db.session.add_all(reviews)
    db.session.commit()

    print('Table Seeding Successful')
