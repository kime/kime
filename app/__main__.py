import os

import quart.flask_patch
from quart import Quart, send_from_directory

from app import controllers, views
from app.extensions import db, auth
from app.services.db import azure
from app import config

# Create and configure the Flask app
app = Quart(__name__)
app.register_blueprint(views.v1.blueprint)
app.register_blueprint(controllers.auth.blueprint)

# Set Quart configs
app.config['SECRET_KEY'] = config.secret_key()
app.config['SESSION_TYPE'] = 'filesystem'

# Register app extensions
auth.init_app(app)
azure.init_app(app, db)


@app.route('/')
async def index():
    return await send_from_directory('docs', 'index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3780))
    app.run(host='0.0.0.0', port=port)
