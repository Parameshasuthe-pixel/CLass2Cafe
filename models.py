from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    roll_number = db.Column(db.String(50))
    whatsapp_number = db.Column(db.String(20), unique=True)
    favorite_foods = db.Column(db.String(200))
    preferred_ordering_time = db.Column(db.String(50))


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean, default=True)
    preparation_time = db.Column(db.Integer)
    customization_options = db.Column(db.String(300))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50))
    token_number = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default="Pending")
    total_amount = db.Column(db.Integer)
    payment_status = db.Column(db.String(50), default="Unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship(
        'OrderItem',
        backref='order',
        lazy=True
    )

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    quantity = db.Column(db.Integer)
    customization = db.Column(db.String(200))

    menu_item = db.relationship(
        'MenuItem',
        backref='order_items'
    )

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    transaction_id = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(50))


class CrowdData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_slot = db.Column(db.String(50))
    crowd_percentage = db.Column(db.Integer)


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favorite_item = db.Column(db.String(100))

class PickupSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slot_time = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
