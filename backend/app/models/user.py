from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.Enum('admin', 'manager', 'staff', name='user_role'), nullable=False, default='staff')
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def get_completed_services_today(self):
        """Get number of services completed by this user today"""
        from datetime import date
        from sqlalchemy import and_
        today = datetime.utcnow().date()
        return OrderService.query.filter(
            and_(
                OrderService.assigned_staff_id == self.id,
                OrderService.status == 'completed',
                db.cast(OrderService.completed_at, db.Date) == today
            )
        ).count()

    def get_active_services(self):
        """Get currently active services assigned to this user"""
        return OrderService.query.filter_by(
            assigned_staff_id=self.id,
            status='in_progress'
        ).all()

    def has_permission(self, permission):
        """Check if user has specific permission based on role"""
        permissions = {
            'admin': ['view_all', 'manage_users', 'manage_settings', 'manage_services', 'view_reports'],
            'manager': ['view_all', 'manage_orders', 'manage_payments', 'view_reports', 'manage_staff'],
            'staff': ['view_own', 'update_assigned', 'record_basic_info']
        }
        return permission in permissions.get(self.role, [])

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'