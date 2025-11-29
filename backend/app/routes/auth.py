from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db, login_manager
from app.models import User
import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        # Handle API login (JSON)
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            remember = data.get('remember', False)
        else:
            # Handle form login
            username = request.form.get('username')
            password = request.form.get('password')
            remember = request.form.get('remember', False)

        # Validate inputs
        if not username or not password:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'VALIDATION_ERROR',
                        'message': 'Username and password are required'
                    },
                    'timestamp': datetime.datetime.utcnow().isoformat()
                }), 400
            else:
                flash('Username and password are required', 'error')
                return redirect(url_for('auth.login'))

        # Find user
        user = User.query.filter_by(username=username).first()

        # Check credentials
        if user and user.is_active and check_password_hash(user.password_hash, password):
            # Successful login
            login_user(user, remember=bool(remember))
            user.update_last_login()

            if request.is_json:
                return jsonify({
                    'success': True,
                    'data': {
                        'user': user.to_dict(),
                        'next_url': url_for('main.dashboard')
                    },
                    'message': 'Login successful',
                    'timestamp': datetime.datetime.utcnow().isoformat()
                })
            else:
                # Check for next page
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('main.dashboard'))
        else:
            # Failed login
            error_msg = 'Invalid username or password' if user else 'User not found'
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'AUTH_ERROR',
                        'message': error_msg
                    },
                    'timestamp': datetime.datetime.utcnow().isoformat()
                }), 401
            else:
                flash(error_msg, 'error')
                return redirect(url_for('auth.login'))

    # GET request - show login page
    if request.is_json:
        return jsonify({
            'success': False,
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'Please use POST for login'
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 405
    else:
        return render_template('auth/login.html')

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout"""
    if request.is_json:
        # API logout
        logout_user()
        return jsonify({
            'success': True,
            'message': 'Logout successful',
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
    else:
        # Form logout
        logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('auth.login'))

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user profile"""
    if request.is_json:
        return jsonify({
            'success': True,
            'data': {
                'user': current_user.to_dict()
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
    else:
        return render_template('auth/profile.html', user=current_user)

@bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change current user password"""
    if request.is_json:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
    else:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

    # Validate inputs
    if not all([current_password, new_password, confirm_password]):
        error_msg = 'All password fields are required'
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_msg
                }
            }), 400
        else:
            flash(error_msg, 'error')
            return redirect(url_for('auth.profile'))

    if new_password != confirm_password:
        error_msg = 'New passwords do not match'
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_msg
                }
            }), 400
        else:
            flash(error_msg, 'error')
            return redirect(url_for('auth.profile'))

    if len(new_password) < 6:
        error_msg = 'Password must be at least 6 characters long'
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_msg
                }
            }), 400
        else:
            flash(error_msg, 'error')
            return redirect(url_for('auth.profile'))

    # Verify current password
    if not check_password_hash(current_user.password_hash, current_password):
        error_msg = 'Current password is incorrect'
        if request.is_json:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'AUTH_ERROR',
                    'message': error_msg
                }
            }), 401
        else:
            flash(error_msg, 'error')
            return redirect(url_for('auth.profile'))

    # Update password
    current_user.set_password(new_password)
    db.session.commit()

    success_msg = 'Password changed successfully'
    if request.is_json:
        return jsonify({
            'success': True,
            'message': success_msg,
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
    else:
        flash(success_msg, 'success')
        return redirect(url_for('auth.profile'))

@bp.route('/refresh', methods=['POST'])
@login_required
def refresh_session():
    """Refresh user session"""
    current_user.update_last_login()

    if request.is_json:
        return jsonify({
            'success': True,
            'data': {
                'user': current_user.to_dict()
            },
            'message': 'Session refreshed',
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
    else:
        return redirect(url_for('main.dashboard'))

@bp.route('/check', methods=['GET'])
@login_required
def check_session():
    """Check if user session is valid"""
    if request.is_json:
        return jsonify({
            'success': True,
            'data': {
                'user': current_user.to_dict(),
                'session_valid': True
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        })
    else:
        return 'Session is valid', 200

# Error handlers
@bp.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access"""
    if request.is_json:
        return jsonify({
            'success': False,
            'error': {
                'code': 'UNAUTHORIZED',
                'message': 'Please log in to access this resource'
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 401
    else:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('auth.login'))

@bp.errorhandler(403)
def forbidden(error):
    """Handle forbidden access"""
    if request.is_json:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FORBIDDEN',
                'message': 'You do not have permission to access this resource'
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 403
    else:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('main.dashboard'))

@bp.errorhandler(429)
def ratelimit_handler(error):
    """Handle rate limiting"""
    if request.is_json:
        return jsonify({
            'success': False,
            'error': {
                'code': 'RATE_LIMIT_EXCEEDED',
                'message': 'Too many requests. Please try again later.'
            },
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 429
    else:
        flash('Too many requests. Please try again later.', 'error')
        return redirect(url_for('auth.login'))

# Helper functions
def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': 'Admin access required'
                    }
                }), 403
            else:
                flash('Admin access required', 'error')
                return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    """Decorator to require manager or admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'manager']:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'FORBIDDEN',
                        'message': 'Manager access required'
                    }
                }), 403
            else:
                flash('Manager access required', 'error')
                return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def staff_required(f):
    """Decorator to require any authenticated user (staff, manager, admin)"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'UNAUTHORIZED',
                        'message': 'Authentication required'
                    }
                }), 401
            else:
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function