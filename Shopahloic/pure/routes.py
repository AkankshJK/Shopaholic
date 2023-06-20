from pure import app
from flask import render_template, redirect, url_for, flash, request
from pure.models import Product, User, Cart
from pure.forms import Sign_up_Form, LoginForm
from pure import db
from flask_login import login_user, logout_user,UserMixin

@app.route('/')
@app.route('/home')
def home_page():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/shop')
def shop_page():
    products = Product.query.all()
    return render_template('shop.html', products=products)


@app.route('/product')
def product_page():
    return render_template('product.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in_page():
    form = Sign_up_Form()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data, address=form.address.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))

    if form.errors != {}: #If there is no error from the validations
        for err_msg in form.errors.values():
            flash(f'There was an erroe Creating a user: {err_msg}', category='danger')

    return render_template('signin.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not mached! Please try again', category='danger')


    return render_template('login.html', form=form)

@app.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    productId = str(request.args.get('product.id'))
    cart_item = Cart(product_id= productId)
    db.session.add(cart_item)
    db.session.commit()
    return render_template('cart.html', cart_item = cart_item)

@app.route('/cart')
def cart_page():
    cart_items = Cart.query.all()
    return render_template('cart.html', cart_items = cart_items)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been Logged out!", category='info')
    return redirect(url_for('home_page'))

