from datetime import datetime
from app import db

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, index=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    make = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    orders = db.relationship('ServiceOrder', backref='vehicle', lazy='dynamic')

    def __init__(self, customer_id, registration_number, make=None, model=None, color=None):
        self.customer_id = customer_id
        self.registration_number = registration_number.upper()  # Standardize registration numbers
        self.make = make
        self.model = model
        self.color = color

    def get_service_count(self):
        """Get total number of services for this vehicle"""
        return self.orders.filter_by(status='completed').count()

    def get_total_spent(self):
        """Calculate total amount spent on this vehicle"""
        from sqlalchemy import func
        result = db.session.query(func.sum(ServiceOrder.total_amount)).filter_by(
            vehicle_id=self.id,
            status='completed'
        ).scalar()
        return result or 0

    def get_last_service_date(self):
        """Get date of last service"""
        last_order = self.orders.filter_by(status='completed').order_by(
            ServiceOrder.completed_at.desc()
        ).first()
        return last_order.completed_at if last_order else None

    def get_service_history(self, limit=5):
        """Get recent service history"""
        return self.orders.filter_by(status='completed').order_by(
            ServiceOrder.completed_at.desc()
        ).limit(limit).all()

    def get_favorite_services(self, limit=3):
        """Get most frequently used services for this vehicle"""
        from sqlalchemy import func
        from .order_service import OrderService
        from .service import Service

        # Count service occurrences for this vehicle
        service_counts = db.session.query(
            Service.name,
            func.count(OrderService.id).label('count')
        ).join(OrderService).join(ServiceOrder).filter_by(
            vehicle_id=self.id,
            status='completed'
        ).group_by(Service.id, Service.name).order_by(
            func.count(OrderService.id).desc()
        ).limit(limit).all()

        return [{'service': name, 'count': count} for name, count in service_counts]

    def format_registration(self):
        """Format registration number for display"""
        return self.registration_number

    def get_display_name(self):
        """Get full vehicle description"""
        parts = []
        if self.make:
            parts.append(self.make)
        if self.model:
            parts.append(self.model)
        if self.color:
            parts.append(f"({self.color})")

        base_name = ' '.join(parts) if parts else 'Unknown Vehicle'
        return f"{base_name} - {self.format_registration()}"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'registration_number': self.registration_number,
            'make': self.make,
            'model': self.model,
            'color': self.color,
            'display_name': self.get_display_name(),
            'service_count': self.get_service_count(),
            'total_spent': float(self.get_total_spent()),
            'last_service_date': self.get_last_service_date().isoformat() if self.get_last_service_date() else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'favorite_services': self.get_favorite_services()
        }

    @staticmethod
    def normalize_registration(reg_number):
        """Normalize registration number format"""
        if not reg_number:
            return None
        return reg_number.strip().upper().replace(' ', '')

    @staticmethod
    def validate_registration(reg_number):
        """Basic validation for registration number"""
        if not reg_number or len(reg_number.strip()) < 3:
            return False
        return True

    def __repr__(self):
        return f'<Vehicle {self.registration_number} ({self.make} {self.model})>'