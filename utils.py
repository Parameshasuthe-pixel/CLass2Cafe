import random
import string
from datetime import datetime


def generate_order_id():
    """
    Generate unique order ID
    Example: CAF2931
    """
    return "CAF" + ''.join(random.choices(string.digits, k=4))


def generate_token():
    """
    Generate token number
    Example: T41
    """
    return "T" + ''.join(random.choices(string.digits, k=2))


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def calculate_total(cart_items):
    """
    cart_items example:
    [
        {"price": 40, "quantity": 2},
        {"price": 50, "quantity": 1}
    ]
    """

    total = 0

    for item in cart_items:
        total += item["price"] * item["quantity"]

    return total


def crowd_message(crowd_percentage):

    if crowd_percentage >= 80:
        return "⚠️ Peak crowd detected"

    elif crowd_percentage >= 50:
        return "👥 Medium crowd"

    return "✅ Less crowded"


def format_currency(amount):
    return f"₹{amount}"


def welcome_message(name):
    return f'''
Hey {name} 👋

Welcome back to Class2Cafe 🤖🍽️

What can I do for you today?
'''