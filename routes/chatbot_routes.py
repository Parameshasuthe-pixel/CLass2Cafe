from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

from chatbot import process_message

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/webhook", methods=["POST"])
def webhook():

    incoming_msg = request.form.get("Body", "")
    sender = request.form.get("From", "")

    print("MESSAGE:", incoming_msg)

    response_text = process_message(sender, incoming_msg)

    print("RESPONSE:", response_text)

    twilio_response = MessagingResponse()
    twilio_response.message(response_text)

    return str(twilio_response), 200, {"Content-Type": "text/xml"}