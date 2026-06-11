from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/webhook", methods=["POST"])
def webhook():

    print("WEBHOOK HIT", flush=True)

    incoming_msg = request.form.get("Body")
    print("Message:", incoming_msg, flush=True)

    twilio_response = MessagingResponse()
    twilio_response.message("Received: " + str(incoming_msg))

    return str(twilio_response)