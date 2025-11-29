from datetime import datetime
from app import db

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Numeric(10, 2), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    category = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    display_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    order_services = db.relationship('OrderService', backref='service', lazy='dynamic')
    
    # ADD THIS METHOD:
    def to_dict(self, include_stats=False):
        """Convert service to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'base_price': float(self.base_price),
            'duration_minutes': self.duration_minutes,
            'category': self.category,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_stats:
            # Add usage statistics
            data['total_orders'] = self.order_services.count()
            data['total_revenue'] = sum(
                float(os.price_charged) 
                for os in self.order_services 
                if os.status == 'completed'
            )
        
        return data
def __init__(self, name, base_price, duration_minutes=30, description=None, category=None, display_order=0):
    self.name = name
    self.base_price = base_price
    self.duration_minutes = duration_minutes
    self.description = description
    self.category = category  # ← ADD THIS LINE
    self.display_order = display_order
    def get_popularity(self):
        """Get how many times this service has been used"""
        return self.order_services.filter_by(status='completed').count()

    def get_total_revenue(self):
        """Calculate total revenue from this service"""
        from sqlalchemy import func
        result = db.session.query(func.sum(OrderService.price_charged)).filter_by(
            service_id=self.id,
            status='completed'
        ).scalar()
        return float(result) if result else 0

    def get_average_rating(self):
        """Get average customer rating for this service"""
        # Placeholder for future rating system
        return None

    def get_active_assignments(self):
        """Get currently active assignments for this service"""
        from .order_service import OrderService
        return self.order_services.filter_by(status='in_progress').all()

    def get_today_usage(self):
        """Get how many times this service was used today"""
        from sqlalchemy import and_, func, cast, Date
        from .order_service import OrderService

        today = datetime.utcnow().date()
        return db.session.query(OrderService).filter(
            and_(
                OrderService.service_id == self.id,
                OrderService.status == 'completed',
                cast(OrderService.completed_at, Date) == today
            )
        ).count()

    def get_weekly_usage(self):
        """Get usage statistics for the current week"""
        from sqlalchemy import and_, func, extract
        from .order_service import OrderService

        # Get current week number
        current_year = datetime.utcnow().year
        current_week = datetime.utcnow().isocalendar()[1]

        return db.session.query(OrderService).filter(
            and_(
                OrderService.service_id == self.id,
                OrderService.status == 'completed',
                extract('year', OrderService.completed_at) == current_year,
                extract('week', OrderService.completed_at) == current_week
            )
        ).count()

    def get_monthly_revenue(self):
        """Get revenue for current month"""
        from sqlalchemy import and_, func, extract
        from .order_service import OrderService

        current_year = datetime.utcnow().year
        current_month = datetime.utcnow().month

        result = db.session.query(func.sum(OrderService.price_charged)).filter(
            and_(
                OrderService.service_id == self.id,
                OrderService.status == 'completed',
                extract('year', OrderService.completed_at) == current_year,
                extract('month', OrderService.completed_at) == current_month
            )
        ).scalar()

        return float(result) if result else 0

    def update_price(self, new_price):
        """Update service price"""
        self.base_price = new_price
        db.session.commit()

    def toggle_active(self):
        """Toggle service active status"""
        self.is_active = not self.is_active
        db.session.commit()

    def reorder(self, new_order):
        """Update display order"""
        self.display_order = new_order
        db.session.commit()

def to_dict(self, include_stats=False):
    """Convert to dictionary for API responses"""
    result = {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'base_price': float(self.base_price),
        'duration_minutes': self.duration_minutes,
        'category': self.category,
        'is_active': self.is_active,
        'display_order': self.display_order,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }

    if include_stats:
        result.update({
            'popularity': self.get_popularity(),
            'total_revenue': self.get_total_revenue(),
            'today_usage': self.get_today_usage(),
            'weekly_usage': self.get_weekly_usage(),
            'monthly_revenue': self.get_monthly_revenue(),
            'active_assignments': len(self.get_active_assignments())
        })

    return result

    @staticmethod
    def get_active_services():
        """Get all active services ordered by display order"""
        return Service.query.filter_by(is_active=True).order_by(Service.display_order, Service.name).all()

    @staticmethod
    def get_popular_services(limit=5):
        """Get most popular services"""
        from sqlalchemy import func
        from .order_service import OrderService

        services_with_counts = db.session.query(
            Service,
            func.count(OrderService.id).label('count')
        ).join(OrderService).filter_by(
            status='completed'
        ).group_by(Service.id).order_by(
            func.count(OrderService.id).desc()
        ).limit(limit).all()

        return [{'service': service.to_dict(), 'count': count} for service, count in services_with_counts]

    def __repr__(self):
        return f'<Service {self.name} (KES {self.base_price})>'