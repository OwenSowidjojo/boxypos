from flask import Blueprint, render_template, request, redirect, url_for
from .models import Product
from . import db
from print.printer import print_order  # NEW

bp = Blueprint('main', __name__)

@bp.route('/menu')
def menu():
    products = Product.query.all()
    return render_template('menu.html', products=products)

@bp.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')

    if name and price:
        try:
            price = float(price)
            product = Product(name=name, price=price)
            db.session.add(product)
            db.session.commit()

            print_order(name, price)  # NEW
        except ValueError:
            pass

    return redirect(url_for('m/.ain.menu'))
