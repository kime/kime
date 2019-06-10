from app.extensions import db


class OriginalImage(db.Model):
    __tablename__ = 'original_image'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')

    @staticmethod
    def add_image(url, name, user):
        """

        :param url:
        :param name:
        :param user:
        :return:
        """
        image = OriginalImage(url=url, name=name, user_id=user.id)
        image.user = user

        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def remove_image(image_id):
        """

        :param image_id:
        :return:
        """
        image = OriginalImage.query.filter(OriginalImage.id == image_id).one()

        db.session.delete(image)
        db.session.commit()
        return image

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
    original_id = db.Column(db.Integer, db.ForeignKey('original_image.id'))

    user = db.relationship('User')
    original_image = db.relationship('OriginalImage')

    @staticmethod
    def add_image(url, user, original_image):
        """

        :param url:
        :param name:
        :param user:
        :param original_image:
        :return:
        """
        image = EnhancedImage(url=url, user_id=user.id, original_id=original_image.id)
        image.user = user
        image.original_image = original_image

        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def remove_image(image_id):
        """

        :param image_id:
        :return:
        """
        image = EnhancedImage.query.filter(EnhancedImage.id == image_id).one()

        db.session.delete(image)
        db.session.commit()
        return image

    @staticmethod
    def get_images(user_id):
        """

        :param user_id:
        :return:
        """
        return EnhancedImage.query.filter(EnhancedImage.user_id == user_id).all()
