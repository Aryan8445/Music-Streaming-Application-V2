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
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CACHE_TYPE= 'redis'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_DEFAULT_TIMEOUT= 300
    broker_connection_retry_on_startup=True
    
