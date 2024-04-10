from datetime import timedelta
UPLOAD_FOLDER = "app/static/songs"

class Config():
    SECRET_KEY = "Aryan Bhardwaj"
    UPLOAD_FOLDER = UPLOAD_FOLDER
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = 'musicstreamingapplicationsecretkey'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
