from flask import jsonify


def ok():
    """
    Standard response for successful HTTP requests
    :return: 200 OK
    """
    return 200


def created():
    """
    Response when the request created a new resource
    :return: 201 Created
    """
    return 201


def bad_request(message='Bad Request'):
    """
    Response when the server cannot the request due to an apparent client error
    :param message: explanation of the error situation
    :return: 400 Bad Request
    """
    return jsonify({'message': message}), 400


def forbidden(message='Forbidden'):
    """
    Response when the user might not have the necessary permissions for a resource
    :param message: explanation of the error situation
    :return: 403 Forbidden
    """
    return jsonify({'message': message}), 403


def page_expired(message='Page Expired'):
    """
    Response when the user token is missing or has expired
    :param message: explanation of the error situation
    :return: 419 Page Expired
    """
    return jsonify({'message': message}), 419


def internal_error(message='Internal Server Error'):
    """
    Response given when an unexpected condition was encountered
    :param message: explanation of the error situation
    :return: 500 Internal Server Error
    """
    return jsonify({'message': message}), 500


def not_implemented(message='Not Implemented'):
    """
    Response given when the server lacks the ability to fulfil the request
    :param message: explanation of the error situation
    :return: 501 Not Implemented
    """
    return jsonify({'message': message}), 501
