from app.extensions import db
from app.models import Admin

def setup_initial_data():
    # Check if the admin already exists
    admin = Admin.query.first()
    if admin is None:
        # Create a new admin user
        admin = Admin(name="Admin", email="testadmin@gmail.com", password="14789632")
        db.session.add(admin)
        db.session.commit()
