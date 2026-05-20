from ai_engine import ask_ai
import random
import time

users = {}

menu = {
    "1": ("Samosa", 20),
    "2": ("Sandwich", 45),
    "3": ("Filter Coffee", 25)
}


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
        lines.append(f"• {item['item']} × {item['qty']} = ₹{subtotal}")
    lines.append(f"\n💰 *Total: ₹{total}*")
    return "\n".join(lines)


def get_cart_total(cart):
    return sum(item["price"] * item["qty"] for item in cart)


def process_message(phone, msg):

    msg = msg.strip()

    # NEW USER
    if phone not in users:
        users[phone] = {
            "step": "menu",
            "name": "Customer",
            "cart": [],           # multiple items stored here
            "current_order": {},
            "orders": []
        }

    user = users[phone]

    intent = detect_intent(msg)

    # ─── GREETING (always) ───────────────────────────────────────
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

    # ─── MAIN MENU STEP ──────────────────────────────────────────
    if user["step"] == "menu":

        if intent == "menu":
            user["step"] = "food"
            return (
                "🍽️ *Today's Menu*\n\n"
                "1️⃣ Samosa — ₹20\n"
                "2️⃣ Sandwich — ₹45\n"
                "3️⃣ Filter Coffee — ₹25\n\n"
                "Reply with item name or number 😊"
            )

        elif intent == "crowd":
            return (
                "🟡 Cafeteria is moderately crowded.\n\n"
                "⏰ Average waiting time: 15–20 mins\n\n"
                "✅ Best time to visit: After 2 PM 😊"
                + polite_end()
            )

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

        elif intent == "cancel":
            if not user["orders"]:
                return "❌ No active orders available." + polite_end()
            last = user["orders"].pop()
            return (
                f"✅ Order {last['order_id']} cancelled successfully.\n\n"
                "💰 Refund will be processed shortly."
                + polite_end()
            )

        elif intent == "feedback":
            user["step"] = "feedback"
            return "💬 Please share your feedback 😊"

        elif intent == "recommend":
            if user["orders"]:
                last = user["orders"][-1]
                return (
                    f"⭐ You usually order from our menu 😊\n\n"
                    "Would you like to see the menu again?\n"
                    "Type *menu* to browse 😊"
                )
            return (
                "⭐ Today's Recommendation:\n\n"
                "🥪 Sandwich + ☕ Coffee Combo"
                + polite_end()
            )

        elif intent in ["coffee", "sandwich", "samosa"]:
            # Direct order from menu step
            user["step"] = "food"
            return _handle_food_selection(user, intent)

        else:
            return (
                "😊 I can help you order food, track orders, "
                "check crowd status and more.\n\n"
                "Try:\n"
                "• I need coffee\n"
                "• Show menu\n"
                "• Is cafeteria busy?"
            )

    # ─── FOOD SELECTION STEP ─────────────────────────────────────
    elif user["step"] == "food":

        msg_lower = msg.lower()

        if msg_lower == "1" or "samosa" in msg_lower:
            return _handle_food_selection(user, "samosa")
        elif msg_lower == "2" or "sandwich" in msg_lower:
            return _handle_food_selection(user, "sandwich")
        elif msg_lower == "3" or "coffee" in msg_lower:
            return _handle_food_selection(user, "coffee")
        else:
            return (
                "⚠️ Please select a valid item.\n\n"
                "1️⃣ Samosa — ₹20\n"
                "2️⃣ Sandwich — ₹45\n"
                "3️⃣ Filter Coffee — ₹25"
            )

    # ─── QUANTITY STEP ───────────────────────────────────────────
    elif user["step"] == "quantity":

        if not msg.isdigit() or int(msg) < 1:
            return "⚠️ Please enter a valid quantity (e.g. 1, 2, 3)"

        qty = int(msg)
        item = user["current_order"]["item"]
        price = user["current_order"]["price"]
        subtotal = qty * price

        # Add to cart
        user["cart"].append({
            "item": item,
            "price": price,
            "qty": qty,
            "subtotal": subtotal
        })

        user["step"] = "add_more"

        return (
            f"✅ *{item} × {qty}* added to cart!\n\n"
            f"🛒 *Your Cart:*\n{get_cart_summary(user['cart'])}\n\n"
            "━━━━━━━━━━━━━━\n"
            "Want to add more items?\n\n"
            "1️⃣ Yes, add more\n"
            "2️⃣ No, proceed to checkout"
        )

    # ─── ADD MORE STEP ───────────────────────────────────────────
    elif user["step"] == "add_more":

        if msg == "1" or "yes" in msg.lower():
            user["step"] = "food"
            return (
                "🍽️ *Menu*\n\n"
                "1️⃣ Samosa — ₹20\n"
                "2️⃣ Sandwich — ₹45\n"
                "3️⃣ Filter Coffee — ₹25\n\n"
                "Select item to add 😊"
            )

        elif msg == "2" or "no" in msg.lower():
            user["step"] = "pickup"
            return (
                f"🛒 *Final Cart:*\n{get_cart_summary(user['cart'])}\n\n"
                "━━━━━━━━━━━━━━\n"
                "⏰ Select pickup time:\n\n"
                "1️⃣ 1:00 PM\n"
                "2️⃣ 1:30 PM\n"
                "3️⃣ 2:00 PM"
            )

        else:
            return (
                "Please reply:\n"
                "1️⃣ Yes, add more\n"
                "2️⃣ No, proceed to checkout"
            )

    # ─── PICKUP STEP ─────────────────────────────────────────────
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
            "💳 *Payment Options*\n\n"
            "1️⃣ UPI / QR Code\n"
            "2️⃣ Cash on Pickup"
        )

    # ─── PAYMENT STEP ────────────────────────────────────────────
    elif user["step"] == "payment":

        total = get_cart_total(user["cart"])

        if msg == "1":
            user["step"] = "payment_confirmation"
            return (
                "📱 *UPI Payment*\n\n"
                f"💰 Amount: *₹{total}*\n\n"
                "━━━━━━━━━━━━━━\n"
                "Scan QR Code below 👇\n\n"
                "🔲 *[QR CODE]*\n"
                "┌─────────────┐\n"
                "│  ████ ░░ ██ │\n"
                "│  ░░ █████░░ │\n"
                "│  ██░░░ ████ │\n"
                "│  ░░██ ░░░██ │\n"
                "└─────────────┘\n\n"
                "📲 UPI ID: *class2cafe@upi*\n\n"
                "━━━━━━━━━━━━━━\n"
                "After payment, reply with your\n"
                "*UPI Transaction ID* to confirm ✅"
            )

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
            user["cart"] = []
            user["step"] = "menu"

            return (
                "🎉 *Order Confirmed!*\n\n"
                f"🧾 Order ID: *{order_id}*\n\n"
                f"🛒 Items:\n{get_cart_summary(order['cart'])}\n\n"
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

    # ─── PAYMENT CONFIRMATION STEP ───────────────────────────────
    elif user["step"] == "payment_confirmation":

        # Accept any transaction ID (min 6 chars) or "PAID"
        if len(msg.strip()) < 4:
            return (
                "⚠️ Please enter your *UPI Transaction ID*\n\n"
                "Example: *UPI123456789*\n\n"
                "Or type *PAID* if you don't have the ID handy."
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
            f"🛒 Items:\n{get_cart_summary(order['cart'])}\n\n"
            f"⏰ Pickup: *{order['pickup']}*\n"
            "💳 Payment: *UPI ✅*"
            + polite_end()
        )

    # ─── FEEDBACK STEP ───────────────────────────────────────────
    elif user["step"] == "feedback":
        user["step"] = "menu"
        return (
            "✅ Thank you for your feedback 😊\n\n"
            "We'll keep improving!"
            + polite_end()
        )

    return (
        "⚠️ Something went wrong.\n\n"
        "Please type *hi* to start again."
    )


# ─── HELPER ──────────────────────────────────────────────────────
def _handle_food_selection(user, intent):
    food_map = {
        "samosa": ("Samosa", 20, "🥟"),
        "sandwich": ("Sandwich", 45, "🥪"),
        "coffee": ("Filter Coffee", 25, "☕")
    }
    item, price, emoji = food_map[intent]
    user["current_order"] = {"item": item, "price": price}
    user["step"] = "quantity"
    return f"{emoji} *{item}* selected (₹{price} each)\n\nEnter quantity 😊"