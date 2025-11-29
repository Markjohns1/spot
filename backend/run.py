#!/usr/bin/env python3
"""
Car Wash Management System - Main Application Entry Point
The Spot - Kenya
"""

import os
from app import create_app, db
from app.models import *

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