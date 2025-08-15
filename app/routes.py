from datetime import date, datetime
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func
from .models import Product, Order, OrderItem
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


@bp.route('/new-order', methods=['GET', 'POST'])
def new_order():
    products = Product.query.all()

    if request.method == 'POST':
        table_number = request.form.get('table_number')
        selected_products = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')

        order = Order(timestamp=datetime.utcnow(), total=0.0, table_number=table_number)
        db.session.add(order)
        db.session.flush()  # To get order.id

        total_price = 0.0
        for product_id, qty in zip(selected_products, quantities):
            if qty and int(qty) > 0:
                product = Product.query.get(int(product_id))
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=int(qty)
                )
                db.session.add(order_item)
                total_price += product.price * int(qty)

        order.total = total_price
        db.session.commit()


        return redirect(url_for('main.home'))

    return render_template('new-order.html', products=products)


@bp.route("/history")
def history():
    return render_template('history.html')

@bp.route("/admin")
def admin():
    return render_template('admin.html')

