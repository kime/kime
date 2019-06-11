from flask_testing import TestCase

from app.__main__ import app as kime


class BaseTestCase(TestCase):
    def create_app(self):
        kime.config['TESTING'] = True
        app = kime.App(__name__)
        return app.app
