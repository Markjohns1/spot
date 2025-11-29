from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    # Calculate paths correctly
    current_file = os.path.abspath(__file__)
    app_dir = os.path.dirname(current_file)
    backend_dir = os.path.dirname(app_dir)
    spot_dir = os.path.dirname(backend_dir)
    
    template_dir = os.path.join(spot_dir, 'frontend', 'templates')
    static_dir = os.path.join(spot_dir, 'frontend', 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)  # Add CSRF protection
    login_manager.login_view = 'auth.login'
    
    # Import models
    with app.app_context():
        from app.models import User, Customer, Vehicle, Service, ServiceOrder, OrderService, Payment, StaffAssignment
        db.create_all()
    
    # Register blueprints
    from app.routes import auth, api, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)
    
    # Exempt API routes from CSRF protection
    csrf.exempt(api.bp)  # ← ADD THIS LINE
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    return app