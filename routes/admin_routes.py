from flask import Blueprint, render_template, request, redirect
from models import PickupSlot, db, Order, MenuItem, CrowdData, User


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


# ADD NEW MENU ITEM
@admin_bp.route('/add_menu', methods=['POST'])
def add_menu():

    item = MenuItem(
        item_name=request.form['item_name'],
        category=request.form['category'],
        price=int(request.form['price']),
        availability=True
    )

    db.session.add(item)
    db.session.commit()

    return redirect('/menu')


@admin_bp.route('/crowd')
def crowd_page():
    crowd = CrowdData.query.all()
    return render_template('crowd.html', crowd=crowd)


@admin_bp.route('/analytics')
def analytics_page():
    return render_template('analytics.html')

@admin_bp.route('/complete/<int:order_id>')
def complete_order(order_id):

    order = Order.query.get(order_id)

    if order:

        order.status = "Completed"

        customer = User.query.get(order.user_id)

        if customer:
            print(
                f"NOTIFICATION: Order {order.order_id} completed for {customer.whatsapp_number}"
            )

        db.session.commit()

    return redirect('/orders')

@admin_bp.route('/update_crowd/<status>')
def update_crowd(status):

    crowd = CrowdData.query.first()

    if not crowd:
        crowd = CrowdData(
            time_slot="Current",
            crowd_percentage=0
        )
        db.session.add(crowd)

    if status == "low":
        crowd.crowd_percentage = 20

    elif status == "medium":
        crowd.crowd_percentage = 50

    elif status == "high":
        crowd.crowd_percentage = 90

    db.session.commit()

    return redirect('/crowd')
@admin_bp.route('/delete_menu/<int:item_id>')
def delete_menu(item_id):

    item = MenuItem.query.get(item_id)

    if item:
        db.session.delete(item)
        db.session.commit()

    return redirect('/menu')
@admin_bp.route('/slots')
def slots_page():

    slots = PickupSlot.query.all()

    return render_template(
        'slots.html',
        slots=slots
    )
@admin_bp.route('/add_slot', methods=['POST'])
def add_slot():

    slot = PickupSlot(
        slot_time=request.form['slot_time']
    )

    db.session.add(slot)
    db.session.commit()

    return redirect('/slots')

@admin_bp.route('/delete_slot/<int:slot_id>')
def delete_slot(slot_id):

    slot = PickupSlot.query.get(slot_id)

    if slot:
        db.session.delete(slot)
        db.session.commit()

    return redirect('/slots')