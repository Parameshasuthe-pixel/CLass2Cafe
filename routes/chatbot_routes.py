from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/webhook", methods=["POST"])
def webhook():

    twilio_response = MessagingResponse()
    twilio_response.message("Hello from Class2Cafe!")

    return str(twilio_response)