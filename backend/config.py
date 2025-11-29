import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'car_wash.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    
    # CSRF configuration
    WTF_CSRF_TIME_LIMIT = None
    
    # Business settings
    BUSINESS_NAME = 'The Spot Car Wash'
    BUSINESS_PHONE = '+254712345678'
    BUSINESS_ADDRESS = 'Nairobi, Kenya'
    CURRENCY = 'KES'
    
    # Pagination
    ITEMS_PER_PAGE = 20