from datetime import datetime
from app import db

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    total_visits = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    vehicles = db.relationship('Vehicle', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('ServiceOrder', backref='customer', lazy='dynamic')

    def __init__(self, phone_number, name=None, email=None):
        self.phone_number = phone_number
        self.name = name
        self.email = email

    def increment_visits(self):
        """Increment total visit counter"""
        self.total_visits += 1
        self.updated_at = datetime.utcnow()

    def get_total_spent(self):
        """Calculate total amount spent by this customer"""
        from sqlalchemy import func
        result = db.session.query(func.sum(ServiceOrder.total_amount)).filter_by(
            customer_id=self.id,
            status='completed'
        ).scalar()
        return result or 0

    def get_last_visit_date(self):
        """Get date of last visit"""
        last_order = self.orders.filter_by(status='completed').order_by(
            ServiceOrder.completed_at.desc()
        ).first()
        return last_order.completed_at if last_order else None

    def get_vehicles_list(self):
        """Get all vehicles for this customer"""
        return self.vehicles.all()

    def get_service_history(self, limit=10):
        """Get recent service history"""
        return self.orders.filter_by(status='completed').order_by(
            ServiceOrder.completed_at.desc()
        ).limit(limit).all()

    def is_returning_customer(self):
        """Check if customer has visited before"""
        return self.total_visits > 1

    def update_last_visit(self):
        """Update customer information on new visit"""
        self.increment_visits()
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'email': self.email,
            'total_visits': self.total_visits,
            'total_spent': float(self.get_total_spent()),
            'last_visit_date': self.get_last_visit_date().isoformat() if self.get_last_visit_date() else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_returning': self.is_returning_customer(),
            'vehicles_count': self.vehicles.count()
        }

    def __repr__(self):
        return f'<Customer {self.phone_number} ({self.name})>'