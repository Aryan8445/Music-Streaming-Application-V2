from flask import jsonify
from flask_jwt_extended import  get_jwt_identity
from functools import wraps
from app.models import User, Admin
from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class NotFoundError(HTTPException):
    def __init__(self, status_code, mess):
        self.response = make_response(mess, status_code)


class UnauthorizedError(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 401

# class NotFoundError(Exception):
#     def __init__(self, message):
#         self.message = message
#         self.status_code = 404

class ServerError(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 500

# def handle_custom_exceptions(error):
#     response = jsonify({'message': error.message})
#     response.status_code = error.status_code
#     return response

def creator_or_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()
        admin = Admin.query.filter_by(email=current_user_email).first()

        if current_user and current_user.user_type == "creator":
            return fn(*args, **kwargs)
        elif admin:
            return fn(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    return wrapper