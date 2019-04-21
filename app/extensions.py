from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

auth = HTTPBasicAuth()
db = SQLAlchemy()
