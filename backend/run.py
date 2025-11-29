#!/usr/bin/env python3
"""
Car Wash Management System - Main Application Entry Point
The Spot - Kenya
"""

import os
from app import create_app, db
from app.models import *

basedir = os.path.abspath(os.path.dirname(__file__))
if 'DATABASE_URL' not in os.environ or os.environ.get('USE_SQLITE', 'true').lower() == 'true':
    os.environ['DATABASE_URL'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'car_wash.db')

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )