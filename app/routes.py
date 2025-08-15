from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func

from .models import Product, Order
from . import db
from print.printer import print_order

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    # Get today's date
    today = date.today()

    # Get all orders from today
    today_orders = Order.query.filter(func.date(Order.timestamp) == today).all()

    # Calculate total revenue for today
    total_revenue = sum(order.total for order in today_orders)

    # Count total order
    total_orders = len(today_orders)

    return render_template('home.html',
                           total_revenue=total_revenue,
                           total_orders=total_orders)

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