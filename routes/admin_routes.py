from flask import Blueprint, render_template
from models import Order, MenuItem, CrowdData

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def dashboard():
    orders = Order.query.all()
    return render_template('dashboard.html', orders=orders)


@admin_bp.route('/orders')
def orders_page():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)


@admin_bp.route('/menu')
def menu_page():
    items = MenuItem.query.all()
    return render_template('menu.html', items=items)


@admin_bp.route('/crowd')
def crowd_page():
    crowd = CrowdData.query.all()
    return render_template('crowd.html', crowd=crowd)


@admin_bp.route('/analytics')
def analytics_page():
    return render_template('analytics.html')