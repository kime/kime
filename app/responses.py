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


def no_content():
    """
    Response when request was processed without returning any content
    :return: 204 No Content
    """
    return 204


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


def not_found(message='Not Found'):
    """
    Response when the requested resource could not be found
    :param message: explanation of the error situation
    :return: 404 Not Found
    """
    return jsonify({'message': message}), 404


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
