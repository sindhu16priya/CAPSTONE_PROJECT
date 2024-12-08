from flask import Flask
from config import Config
from models import db
from routes import routes
from new_routes2 import new_routes2
from new_routes3 import new_routes3
from new_routes4 import new_routes4
from new_routes5 import new_routes5

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Register Blueprints
app.register_blueprint(routes)
app.register_blueprint(new_routes2)
app.register_blueprint(new_routes3)
app.register_blueprint(new_routes4)
app.register_blueprint(new_routes5)

if __name__ == "__main__":
    app.run(debug=True)