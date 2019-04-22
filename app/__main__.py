import os

from flask import Flask

from app import controllers, views
from app.extensions import db
from app.services.db import azure
from app import config

# Create and configure the Flask app
app = Flask(__name__)
app.register_blueprint(views.v1.blueprint)
app.register_blueprint(controllers.auth.blueprint)

# Set Flask configs
app.config['SECRET_KEY'] = config.secret_key()
app.config['SESSION_TYPE'] = 'filesystem'

# Register DB extension
azure.init_app(app, db)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3780))
    app.run(host='0.0.0.0', port=port)
