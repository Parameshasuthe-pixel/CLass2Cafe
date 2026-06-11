from flask import Flask, render_template
from config import Config
from models import db, MenuItem

from routes.chatbot_routes import chatbot_bp
from routes.admin_routes import admin_bp
from routes.payment_routes import payment_bp

from scheduler import start_scheduler

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(chatbot_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(payment_bp)


@app.route("/")
def home():
    return render_template("chatbot.html")

from flask import request
from twilio.twiml.messaging_response import MessagingResponse

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.form.get("Body")

    resp = MessagingResponse()
    resp.message(f"You said: {incoming_msg}")

    return str(resp)

with app.app_context():
    db.create_all()


#start_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

