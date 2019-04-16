import os

from flask import Flask

from app import controllers, views
from app.extensions import db
from app.services.db import azure

# Create and configure the Flask app
app = Flask(__name__)
app.register_blueprint(views.blueprint)
app.register_blueprint(controllers.auth.blueprint)

# Register DB extension
azure.init_app(app, db)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3780))
    app.run(host='0.0.0.0', port=port)
