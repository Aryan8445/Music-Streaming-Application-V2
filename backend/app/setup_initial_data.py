from app.extensions import db
from app.models import Admin
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
