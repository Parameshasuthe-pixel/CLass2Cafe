from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from chatbot import process_message

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/webhook", methods=["POST"])
def webhook():

    print("WEBHOOK HIT")

    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    print("MESSAGE:", incoming_msg)

    response_text = "Hello from Render bot!"

    print("RESPONSE:", response_text)

    response = MessagingResponse()
    response.message(response_text)

    return str(response), 200, {
        "Content-Type": "application/xml"
    }