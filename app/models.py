from datetime import datetime
from . import db

# --- Product Model ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    # Relationship
    order_items = db.relationship('OrderItem', back_populates='product')

    def __repr__(self):
        return f"<Product {self.name}>"


# --- Order Model ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float)

    # Optional: Table number
    table_number = db.Column(db.String(10))

    # Relationship
    items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id} - Table {self.table_number} - ${self.total:.2f}>"


# --- OrderItem (Link between Order and Product) ---
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"<OrderItem {self.quantity} x {self.product.name} (Order {self.order_id})>"
