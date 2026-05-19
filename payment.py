import qrcode


def generate_upi_qr(upi_id, amount):
    upi_link = f"upi://pay?pa={upi_id}&am={amount}&cu=INR"

    qr = qrcode.make(upi_link)
    qr.save("static/payment_qr.png")

    return "static/payment_qr.png"