from app import config
from app.models import user


def init_app(app, db):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.azure_db()
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()
