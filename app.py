from flask import Flask
from config import Config
from models import db, MenuItem

from routes.chatbot_routes import chatbot_bp
from routes.admin_routes import admin_bp
from routes.payment_routes import payment_bp

from scheduler import start_scheduler


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Register routes
app.register_blueprint(chatbot_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(payment_bp)


with app.app_context():

    db.create_all()

    # Insert menu items only once
    if not MenuItem.query.first():

        items = [

            MenuItem(
                item_name="Sandwich",
                category="Snacks",
                price=45,
                preparation_time=10,
                customization_options="Extra butter, Cheese add-on"
            ),

            MenuItem(
                item_name="Samosa",
                category="Snacks",
                price=40,
                preparation_time=5,
                customization_options="Extra spicy"
            ),

            MenuItem(
                item_name="Filter Coffee",
                category="Drinks",
                price=25,
                preparation_time=5,
                customization_options="Strong coffee"
            )

        ]

        db.session.bulk_save_objects(items)
        db.session.commit()


start_scheduler()


if __name__ == "__main__":
    app.run(debug=True)