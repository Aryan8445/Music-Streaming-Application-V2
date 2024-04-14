# auth.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Admin

auth = Blueprint('auth', __name__)

from datetime import datetime, timedelta

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, user_type='user').first()
    creator = User.query.filter_by(email=email, user_type='creator').first()
    admin = Admin.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        if user.is_blacklisted:
            return jsonify({'message': 'User is blacklisted. Contact admin for assistance.'}), 403
        access_token = create_access_token(identity=email)
        expires = datetime.utcnow() + timedelta(hours=24)  
        return jsonify({
            'access_token': access_token,
            'user_type': 'user',
            'expires_at': expires,
            'email': user.email  
        }), 200
    elif admin and check_password_hash(admin.password, password):
        access_token = create_access_token(identity=email)
        expires = datetime.utcnow() + timedelta(hours=24)  
        return jsonify({
            'access_token': access_token,
            'user_type': 'admin',
            'expires_at': expires,
            'email': admin.email 
        }), 200
    elif creator and check_password_hash(creator.password, password):
        if creator.is_blacklisted:
            return jsonify({'message': 'Creator is blacklisted. Contact admin for assistance.'}), 403
        access_token = create_access_token(identity=email)
        expires = datetime.utcnow() + timedelta(hours=24)  
        return jsonify({
            'access_token': access_token,
            'user_type': 'creator',
            'expires_at': expires,
            'email': creator.email  
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    firstname = data.get('firstName')
    lastname = data.get('lastName')
    password1 = data.get('password1')
    password2 = data.get('password2')
    user_type = data.get('userRole')

    # Check if passwords match
    if password1 != password2:
        return jsonify({'message': 'Passwords do not match'}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_user or existing_admin:
        return jsonify({'message': 'Email already exists'}), 400

    if len(password1) < 4:
        return jsonify({'message': 'Password must be at least 4 characters long'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password1)

    # Create new user
    new_user = User(email=email, firstname=firstname, lastname=lastname, password=hashed_password, user_type=user_type)
    new_user.save()

    # Generate access token
    access_token = create_access_token(identity=email)
    expires = datetime.utcnow() + timedelta(hours=24)
    return jsonify({'message': 'User created successfully', 'access_token': access_token, 'expires_at': expires}), 201

from datetime import datetime

@auth.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email, user_type='user').first()
    creator = User.query.filter_by(email=current_user_email, user_type='creator').first()
    admin = Admin.query.filter_by(email=current_user_email).first()

    if user:
        registration_date_str = user.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'email': user.email, 'user_type': user.user_type, 'name': f"{user.firstname} {user.lastname}", 'registration_date': registration_date_str}), 200
    elif admin:
        registration_date_str = admin.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'email': admin.email, 'user_type': 'admin', 'name': admin.name, 'registration_date': registration_date_str}), 200
    elif creator:
        registration_date_str = creator.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({'email': creator.email, 'user_type': creator.user_type, 'name': f"{creator.firstname} {creator.lastname}", 'registration_date': registration_date_str}), 200
    else:
        return jsonify({'message': 'User not found'}), 404



@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401