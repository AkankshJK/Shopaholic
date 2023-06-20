from pure import db, login_manager
from pure import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=40),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    address = db.Column(db.String(length=120),nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    catagories = db.Column(db.String(length=120))
    brand = db.Column(db.String(length=50))
    stock = db.Column(db.Integer())
    description = db.Column(db.String(length=120), nullable=False, unique=True)
    img = db.Column(db.String(length=60),nullable=False, unique=True)

class Cart(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    product_id = db.Column(db.Integer(), nullable = False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Cart {self.id}>'