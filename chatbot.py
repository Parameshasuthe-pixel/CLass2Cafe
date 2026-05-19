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

    msg = msg.lower()

    # greetings
    if any(word in msg for word in [
        "hi", "hello", "hey", "bro", "dude"
    ]):
        return "greeting"

    # menu
    elif any(word in msg for word in [
        "menu", "hungry", "food", "eat"
    ]):
        return "menu"

    # coffee
    elif any(word in msg for word in [
        "coffee", "tea", "drink"
    ]):
        return "coffee"

    # sandwich
    elif "sandwich" in msg:
        return "sandwich"

    # samosa
    elif "samosa" in msg:
        return "samosa"

    # crowd
    elif any(word in msg for word in [
        "crowd", "busy", "rush", "waiting"
    ]):
        return "crowd"

    # cancel
    elif "cancel" in msg:
        return "cancel"

    # track
    elif any(word in msg for word in [
        "track", "status"
    ]):
        return "track"

    # feedback
    elif any(word in msg for word in [
        "feedback", "suggestion"
    ]):
        return "feedback"

    # recommend
    elif any(word in msg for word in [
        "recommend", "suggest"
    ]):
        return "recommend"

    return "unknown"


def process_message(phone, msg):

    msg = msg.strip()

    intent = detect_intent(msg)

    # NEW USER
    if phone not in users:

        users[phone] = {
            "step": "menu",
            "name": "Customer",
            "current_order": {},
            "orders": []
        }

    user = users[phone]

    # GREETING
    if intent == "greeting":

        return (
            "👋 Hey! Welcome to *Class2Cafe* 😊\n\n"
            "How can I help you today?"
        )

    # MAIN MENU
    if user["step"] == "menu":

        # MENU
        if intent == "menu":

            user["step"] = "food"

            return (
                "🍽️ Today's Menu\n\n"
                "1️⃣ Samosa — ₹20\n"
                "2️⃣ Sandwich — ₹45\n"
                "3️⃣ Filter Coffee — ₹25\n\n"
                "Reply with item name or number 😊"
            )

        # CROWD
        elif intent == "crowd":

            return (
                "🟡 Cafeteria is moderately crowded.\n\n"
                "⏰ Average waiting time: 15–20 mins\n\n"
                "✅ Best time to visit: After 2 PM 😊"
                + polite_end()
            )

        # TRACK
        elif intent == "track":

            if not user["orders"]:

                return (
                    "📭 No active orders found."
                    + polite_end()
                )

            last = user["orders"][-1]

            return (
                f"🧾 Order ID: {last['order_id']}\n\n"
                f"🍽️ {last['item']} × {last['qty']}\n\n"
                "🟡 Your order is being prepared 😊"
                + polite_end()
            )

        # CANCEL
        elif intent == "cancel":

            if not user["orders"]:

                return (
                    "❌ No active orders available."
                    + polite_end()
                )

            last = user["orders"].pop()

            return (
                f"✅ Order {last['order_id']} cancelled successfully.\n\n"
                "💰 Refund will be processed shortly."
                + polite_end()
            )

        # FEEDBACK
        elif intent == "feedback":

            user["step"] = "feedback"

            return (
                "💬 Please share your feedback 😊"
            )

        # RECOMMEND
        elif intent == "recommend":

            if user["orders"]:

                last = user["orders"][-1]

                return (
                    f"⭐ You usually order {last['item']} 😊\n\n"
                    "Would you like to reorder it today?"
                )

            return (
                "⭐ Today's Recommendation:\n\n"
                "🥪 Sandwich + ☕ Coffee Combo"
                + polite_end()
            )

        # DIRECT FOOD ORDER
        elif intent == "coffee":

            user["current_order"] = {
                "item": "Filter Coffee",
                "price": 25
            }

            user["step"] = "quantity"

            return (
                "☕ Filter Coffee selected.\n\n"
                "Enter quantity 😊"
            )

        elif intent == "sandwich":

            user["current_order"] = {
                "item": "Sandwich",
                "price": 45
            }

            user["step"] = "quantity"

            return (
                "🥪 Sandwich selected.\n\n"
                "Enter quantity 😊"
            )

        elif intent == "samosa":

            user["current_order"] = {
                "item": "Samosa",
                "price": 20
            }

            user["step"] = "quantity"

            return (
                "🥟 Samosa selected.\n\n"
                "Enter quantity 😊"
            )

        else:

            return (
                "😊 I can help you order food, track orders, "
                "check crowd status and more.\n\n"
                "Try:\n"
                "• I need coffee\n"
                "• Show menu\n"
                "• Is cafeteria busy?"
            )

    # FOOD STEP
    elif user["step"] == "food":

        msg = msg.lower()

        if msg == "1" or "samosa" in msg:

            item = "Samosa"
            price = 20

        elif msg == "2" or "sandwich" in msg:

            item = "Sandwich"
            price = 45

        elif msg == "3" or "coffee" in msg:

            item = "Filter Coffee"
            price = 25

        else:

            return (
                "⚠️ Please select a valid item.\n\n"
                "1️⃣ Samosa\n"
                "2️⃣ Sandwich\n"
                "3️⃣ Filter Coffee"
            )

        user["current_order"] = {
            "item": item,
            "price": price
        }

        user["step"] = "quantity"

        return (
            f"✅ {item} selected.\n\n"
            "Enter quantity 😊"
        )

    # QUANTITY
    elif user["step"] == "quantity":

        if not msg.isdigit():

            return "⚠️ Please enter valid quantity."

        qty = int(msg)

        item = user["current_order"]["item"]
        price = user["current_order"]["price"]

        total = qty * price

        user["current_order"]["qty"] = qty
        user["current_order"]["total"] = total

        user["step"] = "pickup"

        return (
            "🧾 Order Summary\n\n"
            f"🍽️ {item} × {qty}\n"
            f"💰 Total: ₹{total}\n\n"
            "Select pickup time:\n\n"
            "1️⃣ 1:00 PM\n"
            "2️⃣ 1:30 PM\n"
            "3️⃣ 2:00 PM"
        )

    # PICKUP
        # PICKUP
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

        return (
            "💳 Payment Options\n\n"
            "1️⃣ UPI Payment\n"
            "2️⃣ Cash on Pickup\n\n"
            "Reply with payment option 😊"
        )

    # PAYMENT
    elif user["step"] == "payment":

        # UPI
        if msg == "1":

            user["step"] = "payment_done"

            return (
                "💳 Please pay using UPI\n\n"
                "📱 UPI ID:\n"
                "class2cafe@upi\n\n"
                "After payment reply:\n"
                "PAID"
            )

        # CASH
        elif msg == "2":

            order_id = generate_order_id()

            order = {
                "order_id": order_id,
                "item": user["current_order"]["item"],
                "qty": user["current_order"]["qty"],
                "total": user["current_order"]["total"],
                "pickup": user["current_order"]["pickup"],
                "time": time.time(),
                "payment": "Cash"
            }

            user["orders"].append(order)

            user["step"] = "menu"

            return (
                "🎉 Order Confirmed!\n\n"
                f"🧾 Order ID: {order_id}\n"
                f"🍽️ {order['item']} × {order['qty']}\n"
                f"💰 Total: ₹{order['total']}\n"
                f"⏰ Pickup Time: {order['pickup']}\n"
                "💵 Payment: Cash on Pickup"
                + polite_end()
            )

        else:

            return (
                "⚠️ Select valid payment option.\n\n"
                "1️⃣ UPI Payment\n"
                "2️⃣ Cash on Pickup"
            )

    # PAYMENT DONE
    elif user["step"] == "payment_done":

        if msg.lower() != "paid":

            return (
                "⚠️ After payment type:\n\n"
                "PAID"
            )

        order_id = generate_order_id()

        order = {
            "order_id": order_id,
            "item": user["current_order"]["item"],
            "qty": user["current_order"]["qty"],
            "total": user["current_order"]["total"],
            "pickup": user["current_order"]["pickup"],
            "time": time.time(),
            "payment": "UPI"
        }

        user["orders"].append(order)

        user["step"] = "menu"

        return (
            "🎉 Payment Successful!\n\n"
            "✅ Order Confirmed\n\n"
            f"🧾 Order ID: {order_id}\n"
            f"🍽️ {order['item']} × {order['qty']}\n"
            f"💰 Total: ₹{order['total']}\n"
            f"⏰ Pickup Time: {order['pickup']}\n"
            "💳 Payment: UPI"
            + polite_end()
        )

        

      

    # FEEDBACK
    elif user["step"] == "feedback":

        user["step"] = "menu"

        return (
            "✅ Thank you for your feedback 😊"
            + polite_end()
        )

    return (
        "⚠️ Something went wrong.\n\n"
        "Please try again."
    )