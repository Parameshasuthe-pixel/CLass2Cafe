from flask import Blueprint, jsonify
from payment import generate_upi_qr
from config import Config

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/payment/<amount>')
def payment(amount):
    qr_path = generate_upi_qr(Config.UPI_ID, amount)

    return jsonify({
        "message": "QR Generated",
        "qr": qr_path,
        "upi": Config.UPI_ID
    })