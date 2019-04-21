from app.extensions import db


class OriginalImage(db.Model):
    __tablename__ = 'original_image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    @staticmethod
    def get_images(user_id):
        """

        :param user_id:
        :return:
        """
        return OriginalImage.query.filter(OriginalImage.user_id == user_id).all()


class EnhancedImage(db.Model):
    __tablename__ = 'enhanced_image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    original_id = db.Column(db.Integer, db.ForeignKey('original_image.id'))
    original_image = db.relationship('OriginalImage')

    @staticmethod
    def get_images(user_id):
        """

        :param user_id:
        :return:
        """
        return EnhancedImage.query.filter(EnhancedImage.user_id == user_id).all()
