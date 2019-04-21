from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from passlib.hash import sha512_crypt

from app import config
from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(120))

    def hash_password(self, password):
        """

        :param password:
        :return:
        """
        self.password_hash = sha512_crypt.encrypt(password)

    def verify_password(self, password):
        """

        :param password:
        :return:
        """
        return sha512_crypt.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        """

        :param expiration:
        :return:
        """
        s = Serializer(config.secret_key(), expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """

        :param token:
        :return:
        """
        try:
            s = Serializer(config.secret_key())
            data = s.loads(token)

        except SignatureExpired:
            return None

        except BadSignature:
            return None

        return User.query.get(data['id'])
