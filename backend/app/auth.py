# auth.py
from datetime import datetime
from flask import Blueprint, jsonify, request, send_from_directory, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User, Admin, db
from datetime import datetime, timedelta
from pytz import timezone
from app.tasks import create_csv
from celery.result import AsyncResult
import logging
import matplotlib.pyplot as plt
from app.models import User, Song
import os


auth = Blueprint('auth', __name__)

IST = timezone('Asia/Kolkata')
UPLOAD_DIRECTORY = 'E:\\IIT Madras Projects\\MAD 2\\Music-Streaming-Application\\backend'


@auth.route('/', methods=['GET'])
def index():
    return "success", 200


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
        login_time = datetime.now(IST)
        user.last_visit = login_time
        db.session.commit()
        return jsonify({
            'access_token': access_token,
            'user_type': 'user',
            'expires_at': expires,
            'email': user.email,
            'last_visit': login_time.strftime('%Y-%m-%d %H:%M:%S')
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
        login_time = datetime.now(IST)
        creator.last_visit = login_time
        db.session.commit()
        return jsonify({
            'access_token': access_token,
            'user_type': 'creator',
            'expires_at': expires,
            'email': creator.email,
            'last_visit': login_time.strftime('%Y-%m-%d %H:%M:%S')
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

    if password1 != password2:
        return jsonify({'message': 'Passwords do not match'}), 400

    existing_user = User.query.filter_by(email=email).first()
    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_user or existing_admin:
        return jsonify({'message': 'Email already exists'}), 400

    if len(password1) < 4:
        return jsonify({'message': 'Password must be at least 4 characters long'}), 400

    hashed_password = generate_password_hash(password1)

    new_user = User(email=email, firstname=firstname, lastname=lastname,
                    password=hashed_password, user_type=user_type)
    new_user.save()

    access_token = create_access_token(identity=email)
    expires = datetime.utcnow() + timedelta(hours=24)
    return jsonify({'message': 'User created successfully', 'access_token': access_token, 'expires_at': expires}), 201


@auth.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(
        email=current_user_email, user_type='user').first()
    creator = User.query.filter_by(
        email=current_user_email, user_type='creator').first()
    admin = Admin.query.filter_by(email=current_user_email).first()

    if user:
        registration_date_str = user.registration_date.strftime(
            '%Y-%m-%d %H:%M:%S')
        return jsonify({'email': user.email, 'user_type': user.user_type, 'name': f"{user.firstname} {user.lastname}", 'registration_date': registration_date_str}), 200
    elif admin:
        registration_date_str = admin.registration_date.strftime(
            '%Y-%m-%d %H:%M:%S')
        return jsonify({'email': admin.email, 'user_type': 'admin', 'name': admin.name, 'registration_date': registration_date_str}), 200
    elif creator:
        registration_date_str = creator.registration_date.strftime(
            '%Y-%m-%d %H:%M:%S')
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


@auth.route('/make-csv', methods=['GET'])
def make_csv():
    output = create_csv.delay()
    return jsonify({'task_id': output.id, 'status': 'processing'})


@auth.route('/get-csv/<task_id>', methods=['GET'])
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        logging.info(f"Attempting to send file: {filename}")
        if filename.endswith('.csv'):
            return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)
        else:
            logging.error(f"Invalid file extension: {filename}")
            return jsonify({"error": "Invalid file extension"}), 400
    else:
        return jsonify({"message": "Task Pending"}), 404

@auth.route('/api/generate_top_genre_graph', methods=['GET'])
def generate_top_genre_graph():
    # Generate Top Genre Graph
    top_genre_data = db.session.query(Song.genre, db.func.count(Song.id)).group_by(Song.genre).all()
    genres = [data[0] for data in top_genre_data]
    counts = [data[1] for data in top_genre_data]

    plt.figure(figsize=(8, 6))
    plt.bar(genres, counts)
    plt.xlabel('Genre')
    plt.ylabel('Count')
    plt.title('Top Genre')

    # Construct the file path using os.path.join
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    image_path = os.path.join(base_path, 'static', 'analytics', 'top_genre.png')

    plt.savefig(image_path)
    plt.close()

    return send_file(image_path, mimetype='image/png')

@auth.route('/api/generate_user_vs_creator_graph', methods=['GET'])
def generate_user_vs_creator_graph():
    # Generate User vs Creator Pie Chart
    user_count = User.query.filter_by(user_type='user').count()
    creator_count = User.query.filter_by(user_type='creator').count()

    plt.figure(figsize=(8, 6))
    labels = ['User', 'Creator']
    sizes = [user_count, creator_count]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('User vs Creator')

    # Construct the file path using os.path.join
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    image_path = os.path.join(base_path, 'static', 'analytics', 'user_vs_creator.png')

    plt.savefig(image_path)
    plt.close()

    return send_file(image_path, mimetype='image/png')