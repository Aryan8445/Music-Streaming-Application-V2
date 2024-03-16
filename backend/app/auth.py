from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Admin

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    admin = Admin.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token, 'user_type': 'user'}), 200
    elif admin and check_password_hash(admin.password, password):
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token, 'user_type': 'admin'}), 200
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

    # Check if passwords match
    if password1 != password2:
        return jsonify({'message': 'Passwords do not match'}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password1)

    # Create new user
    new_user = User(email=email, firstname=firstname, lastname=lastname, password=hashed_password, user_type='user')
    new_user.save()

    # Generate access token
    access_token = create_access_token(identity=email)

    return jsonify({'message': 'User created successfully', 'access_token': access_token}), 201

# Other authentication/authorization routes and functions can be added as needed

@jwt_required()
@auth.route('/protected', methods=['GET'])
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@jwt_required()
@auth.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Successfully logged out'}), 200
