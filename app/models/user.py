from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from passlib.hash import sha512_crypt

from app import config
from app.extensions import db
from app.responses import bad_request


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(120))
    is_authenticated = False
    is_anonymous = False
    is_active = True

    def get_id(self):
        return str(self.id)

    @staticmethod
    def add_user(username, password):
        """

        :param username:
        :param password:
        :return:
        """
        user = User(username=username)
        user.hash_password(password)

        db.session.add(user)
        db.session.commit()
        return user

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

    def change_password(self, old_password, new_password):
        """

        :param oldPassword:
        :param newPassword:
        :return:
        """
        if not self.verify_password(old_password):
            return bad_request()

        self.hash_password(new_password)
        db.session.commit()

    def generate_auth_token(self, expiration=7200):
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
