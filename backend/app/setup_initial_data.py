from app.extensions import db
from app.models import Admin, User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

def setup_initial_data():
    # Check if the admin already exists
    admin = Admin.query.first()
    if admin is None:
        password="14789632"
        email="testadmin@gmail.com"
        hashed_password = generate_password_hash(password)
        admin = Admin(name="Admin", email=email, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
    user = User.query.first()
    if user is None:
        user_password, creator_password="12345678", "12345678"
        user_email, creator_email="testuser@gmail.com", "testcreator@gmail.com"
        user_hashed_password, creator_hashed_password = generate_password_hash(user_password), generate_password_hash(creator_password)
        user = User(firstname="User",lastname = "Test", email=user_email, password=user_hashed_password, user_type='user')
        creator = User(firstname="Creator",lastname = "Test", email=creator_email, password=creator_hashed_password, user_type='creator')
        db.session.add(user)
        db.session.add(creator)
        db.session.commit()