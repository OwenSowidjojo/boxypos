from unicodedata import category

from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product
from . import db
from print.printer import print_order  # NEW

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/menu')
def menu():
    products = Product.query.all()
    return render_template('menu.html', products=products)


@bp.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    category = request.form.get('category')
    price = request.form.get('price')

    if name and price:
        try:
            price = float(price)
            product = Product(name=name, category=category, price=price)
            db.session.add(product)
            db.session.commit()

            print_order(name, price)  # NEW
        except ValueError:
            pass

    return redirect(url_for('main.menu'))


@bp.route('/new-order')
def new_order():
    return render_template('new-order.html')

@bp.route("/history")
def history():
    return render_template('history.html')

@bp.route("/admin")
def admin():
    return render_template('admin.html')

# @bp.route("/new-order")
# def new_order():
#     return render_template('new-order.html')