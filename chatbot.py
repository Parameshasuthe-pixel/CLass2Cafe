from ai_engine import ask_ai
from models import CrowdData, db, User, Order, OrderItem, MenuItem, CrowdData
import random
import time

users = {}



def generate_order_id():
    return "C2C" + str(random.randint(100, 999))


def polite_end():
    return (
        "\n\n━━━━━━━━━━━━━━\n"
        "Thank you for visiting *Class2Cafe* 🤖🍽️\n"
        "Visit us again soon 😊"
    )


def detect_intent(msg):
    return ask_ai(msg)


def get_cart_summary(cart):

    if not cart:
        return "🛒 Cart is empty."

    lines = []
    total = 0

    for item in cart:
        subtotal = item["price"] * item["qty"]
        total += subtotal

        lines.append(
            f"• {item['item']} × {item['qty']} = ₹{subtotal}"
        )

    lines.append(f"\n💰 *Total: ₹{total}*")

    return "\n".join(lines)


def get_cart_total(cart):
    return sum(item["price"] * item["qty"] for item in cart)


def process_message(phone, msg):

    msg = msg.strip()

    # ─────────────────────────────────────────────
    # NEW USER
    # ─────────────────────────────────────────────
    if phone not in users:

        users[phone] = {
            "step": "menu",
            "name": "Customer",
            "cart": [],
            "current_order": {},
            "orders": []
        }

    user = users[phone]

    print("USER STEP:", user["step"])
    print("MESSAGE:", msg)

    intent = detect_intent(msg)

    print("INTENT:", intent)

    # ─────────────────────────────────────────────
    # GREETING
    # ─────────────────────────────────────────────
    if intent == "greeting":

        user["step"] = "menu"
        user["cart"] = []

        return (
            "👋 Hey! Welcome to *Class2Cafe* 😊\n\n"
            "How can I help you today?\n\n"
            "Try:\n"
            "• Show menu\n"
            "• I want coffee\n"
            "• Is cafeteria busy?"
        )

    # ─────────────────────────────────────────────
    # MAIN MENU
    # ─────────────────────────────────────────────
    if user["step"] == "menu":

        # SHOW MENU
        if intent == "menu":

            user["step"] = "food"

            items=MenuItem.query.filter_by(availability=True).all()
            menu_text="🍽️ *Menu*\n\n"
            for i, item in enumerate(items,start=1):
                menu_text+=f"{i}.{item.item_name}-₹{item.price}\n"
            menu_text+="\nSelect item😊"
            return menu_text
        
        elif intent=="crowd":
            crowd=CrowdData.query.first()
            if not crowd:
                return ("📊 Crowd data not available." + polite_end()
                )
            percentage=crowd.crowd_percentage
            if percentage<30:
                status="🟢 Not Busy"
                wait_time="5-10 mins"
            else:
                status="🔴 Busy"
                wait_time="15-30 mins"
            return(f"{status}\n\n"
                   f"👥Occupancy:{percentage}%\n\n"
                   f"⌛ Estimated Wait Time:{wait_time}"
                   + polite_end
                   )

        
        # TRACK ORDER
        elif intent == "track":

            if not user["orders"]:
                return "📭 No active orders found." + polite_end()

            last = user["orders"][-1]

            return (
                f"🧾 Order ID: {last['order_id']}\n\n"
                f"🍽️ Items:\n{get_cart_summary(last['cart'])}\n\n"
                "🟡 Your order is being prepared 😊"
                + polite_end()
            )

        # CANCEL ORDER
        elif intent == "cancel":

            if not user["orders"]:
                return "❌ No active orders available." + polite_end()

            last = user["orders"].pop()

            return (
                f"✅ Order {last['order_id']} cancelled successfully.\n\n"
                "💰 Refund will be processed shortly."
                + polite_end()
            )

        # FEEDBACK
        elif intent == "feedback":

            user["step"] = "feedback"

            return "💬 Please share your feedback 😊"

        # RECOMMENDATION
        elif intent == "recommend":

            items=MenuItem.query.filter_by(availability=True).limit(3).all()
            if not items:
                return "⚠️ No items available right now"
            text="⭐ *Recommended Items*\n\n"
            for item in items:
                text+=f"🍽️ {item.item_name}-₹{item.price}\n"
            return text +polite_end()

        # DIRECT ORDER
        elif intent !="unknown":
            items=MenuItem.query.filter_by(availability=True).all()
            for item in items:
                if intent==item.item_name.lower() in msg.lower():
                    user["current_order"]={
                        "item":item.item_name,
                        "price":item.price
                    }
                    user["step"]="quantity"
                    return(
                        f"🍽️ *{item.item_name}* selected\n"
                        f"💰 Price:Rs.{item.price}\n\n"
                        "Enter quantity 😊"
                    )

        # UNKNOWN
        else:

            return (
                "😊 I can help you with:\n\n"
                "• Food ordering\n"
                "• Tracking orders\n"
                "• Crowd status\n"
                "• Recommendations\n\n"
                "Try:\n"
                "• Show menu\n"
                "• I want coffee\n"
                "• Is cafeteria busy?"
            )

    # ─────────────────────────────────────────────
    # FOOD SELECTION
    # ─────────────────────────────────────────────
    elif user["step"] == "food":

        msg_lower = msg.lower().strip()
        items=MenuItem.query.filter_by(availability=True).all()
        if msg_lower.isdigit():
            index=int(msg_lower)-1
            if 0<=index<len(items):
                item=items[index]
                user["current_order"]={
                    "item":item.item_name,
                    "price":item.price
                }
                user["step"]="quantity"
                return(
                    f"🍽️ *{item.item_name}* selected\n"
                    f"💰 Price:Rs.{item.price}\n\n"
                    "Enter quantity 😊"
                )
        for item in items:
            if msg_lower==item.item_name.lower():
                user["current_order"]={
                    "item":item.item_name,
                    "price":item.price
                }
                user["step"]="quantity"
                return(
                    f"🍽️ *{item.item_name}* selected\n"
                    f"💰 Price:Rs.{item.price}\n\n"
                    "Enter quantity 😊"
                )
        return"⚠️Please enter a valid item from the menu"
        
            

    # ─────────────────────────────────────────────
    # QUANTITY
    # ─────────────────────────────────────────────
    elif user["step"] == "quantity":

        if not msg.isdigit() or int(msg) < 1:

            return (
                "⚠️ Please enter a valid quantity.\n\n"
                "Example: 1, 2, 3"
            )

        qty = int(msg)

        item = user["current_order"]["item"]
        price = user["current_order"]["price"]

        subtotal = qty * price

        user["cart"].append({
            "item": item,
            "price": price,
            "qty": qty,
            "subtotal": subtotal
        })

        user["step"] = "add_more"

        return (
            f"✅ *{item} × {qty}* added to cart!\n\n"
            f"🛒 *Your Cart:*\n"
            f"{get_cart_summary(user['cart'])}\n\n"
            "━━━━━━━━━━━━━━\n"
            "Want to add more items?\n\n"
            "1️⃣ Yes\n"
            "2️⃣ No, proceed to checkout"
        )

    # ─────────────────────────────────────────────
    # ADD MORE
    # ─────────────────────────────────────────────
    elif user["step"] == "add_more":

        msg_lower = msg.lower().strip()

        if msg == "1" or msg_lower == "yes":

            user["step"] = "food"
            items= MenuItem.query.filter_by(availability=True).all()
            menu_text="🍽️ *Menu*\n\n"
            for i, item in enumerate(items,start=1):
                menu_text+=f"{i}.{item.item_name}-₹{item.price}\n"
            menu_text+="\nSelect item😊"
            return menu_text
            

            

        elif msg == "2" or msg_lower == "no":

            user["step"] = "pickup"

            return (
                f"🛒 *Final Cart:*\n"
                f"{get_cart_summary(user['cart'])}\n\n"
                "━━━━━━━━━━━━━━\n"
                "⏰ Select pickup time:\n\n"
                "1️⃣ 1:00 PM\n"
                "2️⃣ 1:30 PM\n"
                "3️⃣ 2:00 PM"
            )

        else:

            return (
                "⚠️ Please reply properly.\n\n"
                "1️⃣ Yes\n"
                "2️⃣ No"
            )

    # ─────────────────────────────────────────────
    # PICKUP
    # ─────────────────────────────────────────────
    elif user["step"] == "pickup":

        slots = {
            "1": "1:00 PM",
            "2": "1:30 PM",
            "3": "2:00 PM"
        }

        if msg not in slots:

            return (
                "⚠️ Select valid pickup slot.\n\n"
                "1️⃣ 1:00 PM\n"
                "2️⃣ 1:30 PM\n"
                "3️⃣ 2:00 PM"
            )

        pickup = slots[msg]

        user["current_order"]["pickup"] = pickup

        user["step"] = "payment"

        total = get_cart_total(user["cart"])

        return (
            f"⏰ Pickup at *{pickup}*\n\n"
            f"💰 Total Amount: *₹{total}*\n\n"
            "━━━━━━━━━━━━━━\n"
            "💳 Payment Options\n\n"
            "1️⃣ UPI / QR Code\n"
            "2️⃣ Cash on Pickup"
        )

    # ─────────────────────────────────────────────
    # PAYMENT
    # ─────────────────────────────────────────────
    elif user["step"] == "payment":

        total = get_cart_total(user["cart"])

        # UPI
        if msg == "1":

            user["step"] = "payment_confirmation"

            return (
                "📱 *UPI Payment*\n\n"
                f"💰 Amount: *₹{total}*\n\n"
                "━━━━━━━━━━━━━━\n"
                "📲 UPI ID: *kavananayak40@okaxis*\n\n"
                "After payment,\n"
                "reply with Transaction ID ✅"
            )

        # CASH
        elif msg == "2":

            order_id = generate_order_id()

            order = {
                "order_id": order_id,
                "cart": user["cart"].copy(),
                "total": total,
                "pickup": user["current_order"]["pickup"],
                "time": time.time(),
                "payment": "Cash"
            }

            user["orders"].append(order)
            customer = User.query.filter_by(whatsapp_number=phone).first()
            if not customer:
                customer=User(name="Customer",whatsapp_number=phone)
                db.session.add(customer)
                db.session.commit()
            db_order=Order(order_id=order_id,
                           token_number=order_id,
                           user_id=customer.id,
                           total_amount=total,
                           payment_status="Unpaid",
                           status="Pending"
            )
            db.session.add(db_order)
            db.session.commit()
            for cart_item in order["cart"]:
                menu_item=MenuItem.query.filter_by(item_name=cart_item["item"]).first()
                if menu_item:
                    order_item=OrderItem(order_id=db_order.id,
                                         menu_item_id=menu_item.id,
                                         quantity=cart_item["qty"],
                                         customization=""
                    )
                    db.session.add(order_item)
            db.session.commit()


            user["cart"] = []

            user["step"] = "menu"

            return (
                "🎉 *Order Confirmed!*\n\n"
                f"🧾 Order ID: *{order_id}*\n\n"
                f"🛒 Items:\n"
                f"{get_cart_summary(order['cart'])}\n\n"
                f"⏰ Pickup: *{order['pickup']}*\n"
                "💵 Payment: *Cash on Pickup*\n\n"
                "Please pay at the counter 😊"
                + polite_end()
            )

        else:

            return (
                "⚠️ Select valid payment option.\n\n"
                "1️⃣ UPI / QR Code\n"
                "2️⃣ Cash on Pickup"
            )

    # ─────────────────────────────────────────────
    # PAYMENT CONFIRMATION
    # ─────────────────────────────────────────────
    elif user["step"] == "payment_confirmation":

        if len(msg.strip()) < 4:

            return (
                "⚠️ Please enter valid Transaction ID.\n\n"
                "Example: UPI12345"
            )

        txn_id = msg.strip().upper()

        total = get_cart_total(user["cart"])

        order_id = generate_order_id()

        order = {
            "order_id": order_id,
            "cart": user["cart"].copy(),
            "total": total,
            "pickup": user["current_order"]["pickup"],
            "time": time.time(),
            "payment": "UPI",
            "txn_id": txn_id
        }

        user["orders"].append(order)

        user["cart"] = []

        user["step"] = "menu"

        return (
            "✅ *Payment Confirmed!*\n\n"
            "🎉 *Order Placed Successfully!*\n\n"
            f"🧾 Order ID: *{order_id}*\n"
            f"💳 Txn ID: *{txn_id}*\n\n"
            f"🛒 Items:\n"
            f"{get_cart_summary(order['cart'])}\n\n"
            f"⏰ Pickup: *{order['pickup']}*\n"
            "💳 Payment: *UPI ✅*"
            + polite_end()
        )

    # ─────────────────────────────────────────────
    # FEEDBACK
    # ─────────────────────────────────────────────
    elif user["step"] == "feedback":

        user["step"] = "menu"

        return (
            "✅ Thank you for your feedback 😊\n\n"
            "We'll keep improving!"
            + polite_end()
        )

    # ─────────────────────────────────────────────
    # FALLBACK
    # ─────────────────────────────────────────────
    return (
        "⚠️ Something went wrong.\n\n"
        "Please type *hi* to restart."
    )

