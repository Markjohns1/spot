from datetime import datetime
from app import db

class ServiceOrder(db.Model):
    __tablename__ = 'service_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False, index=True)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', 'cancelled', name='order_status'),
                        default='pending', nullable=False, index=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    amount_paid = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    payment_status = db.Column(db.Enum('unpaid', 'partial', 'paid', 'overpaid', name='payment_status'),
                                default='unpaid', nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    order_services = db.relationship('OrderService', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, order_number, customer_id, vehicle_id, created_by, notes=None):
        self.order_number = order_number
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.created_by = created_by
        self.notes = notes

    @staticmethod
    def generate_order_number():
        """Generate unique order number with date and sequence"""
        today = datetime.utcnow().strftime('%Y%m%d')

        # Find the highest sequence number for today
        today_prefix = f'ORD-{today}'
        last_order = ServiceOrder.query.filter(
            ServiceOrder.order_number.like(f'{today_prefix}%')
        ).order_by(ServiceOrder.id.desc()).first()

        if last_order:
            try:
                last_sequence = int(last_order.order_number.split('-')[-1])
                new_sequence = last_sequence + 1
            except (ValueError, IndexError):
                new_sequence = 1
        else:
            new_sequence = 1

        return f'{today_prefix}-{new_sequence:03d}'

    def get_pending_services(self):
        """Get services that are still pending"""
        return self.order_services.filter_by(status='pending').all()

    def get_in_progress_services(self):
        """Get services currently in progress"""
        return self.order_services.filter_by(status='in_progress').all()

    def get_completed_services(self):
        """Get completed services"""
        return self.order_services.filter_by(status='completed').all()

    def get_all_staff_assigned(self):
        """Get all staff members assigned to this order"""
        from .order_service import OrderService
        from .user import User

        staff_ids = db.session.query(OrderService.assigned_staff_id).filter_by(
            order_id=self.id
        ).distinct().all()

        return User.query.filter(User.id.in_([id[0] for id in staff_ids if id[0]])).all()

    def calculate_total(self):
        """Recalculate total amount based on assigned services"""
        from sqlalchemy import func
        result = db.session.query(func.sum(OrderService.price_charged)).filter_by(order_id=self.id).scalar()
        self.total_amount = float(result) if result else 0
        db.session.commit()
        return self.total_amount

    def update_payment_status(self):
        """Update payment status based on amount paid"""
        if self.amount_paid <= 0:
            self.payment_status = 'unpaid'
        elif self.amount_paid < self.total_amount:
            self.payment_status = 'partial'
        elif self.amount_paid == self.total_amount:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'overpaid'
        db.session.commit()

    def get_balance_due(self):
        """Get remaining balance"""
        return float(self.total_amount - self.amount_paid)

    def get_total_paid(self):
        """Get total amount paid"""
        return float(self.amount_paid)

    def add_payment(self, amount, payment_method, recorded_by, transaction_ref=None, notes=None):
        """Add a payment record"""
        from .payment import Payment

        payment = Payment(
            order_id=self.id,
            amount=amount,
            payment_method=payment_method,
            transaction_reference=transaction_ref,
            recorded_by=recorded_by,
            notes=notes
        )

        db.session.add(payment)
        self.amount_paid += amount
        self.update_payment_status()

        return payment

    def start_service(self):
        """Mark order as in progress"""
        if self.status == 'pending':
            self.status = 'in_progress'
            self.started_at = datetime.utcnow()
            db.session.commit()
            return True
        return False

    def complete_service(self):
        """Mark order as completed"""
        if self.status in ['pending', 'in_progress']:
            # Check if all services are completed
            pending_services = self.get_pending_services()
            in_progress_services = self.get_in_progress_services()

            if not pending_services and not in_progress_services:
                self.status = 'completed'
                self.completed_at = datetime.utcnow()
                db.session.commit()

                # Update customer visit statistics
                if self.customer:
                    self.customer.update_last_visit()

                return True
        return False

    def cancel_service(self, reason=None):
        """Cancel the entire order"""
        if self.status in ['pending', 'in_progress']:
            self.status = 'cancelled'
            if reason:
                self.notes = f"{self.notes or ''}\n\nCancelled: {reason}" if self.notes else f"Cancelled: {reason}"
            db.session.commit()
            return True
        return False

    def get_duration_so_far(self):
        """Calculate duration from start to now"""
        if self.started_at:
            if self.completed_at:
                return self.completed_at - self.started_at
            else:
                return datetime.utcnow() - self.started_at
        return None

    def get_service_summary(self):
        """Get summary of services in this order"""
        services = []
        for order_service in self.order_services:
            services.append({
                'service_name': order_service.service.name if order_service.service else 'Unknown',
                'price': float(order_service.price_charged),
                'status': order_service.status,
                'assigned_staff': order_service.assigned_staff.full_name if order_service.assigned_staff else None,
                'started_at': order_service.started_at.isoformat() if order_service.started_at else None,
                'completed_at': order_service.completed_at.isoformat() if order_service.completed_at else None
            })
        return services

    def is_overdue(self, max_hours=4):
        """Check if order is taking longer than expected"""
        if self.status == 'in_progress' and self.started_at:
            duration = datetime.utcnow() - self.started_at
            return duration.total_seconds() > (max_hours * 3600)
        return False

    def to_dict(self, include_details=False):
        """Convert to dictionary for API responses"""
        result = {
            'id': self.id,
            'order_number': self.order_number,
            'customer_id': self.customer_id,
            'vehicle_id': self.vehicle_id,
            'status': self.status,
            'total_amount': float(self.total_amount),
            'amount_paid': float(self.amount_paid),
            'balance_due': self.get_balance_due(),
            'payment_status': self.payment_status,
            'notes': self.notes,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': int(self.get_duration_so_far().total_seconds() / 60) if self.get_duration_so_far() else None
        }

        if include_details:
            result.update({
                'customer': self.customer.to_dict() if self.customer else None,
                'vehicle': self.vehicle.to_dict() if self.vehicle else None,
                'creator': self.creator.to_dict() if self.creator else None,
                'services': self.get_service_summary(),
                'assigned_staff': [staff.to_dict() for staff in self.get_all_staff_assigned()],
                'is_overdue': self.is_overdue(),
                'payment_count': self.payments.count()
            })

        return result

    @staticmethod
    def get_active_orders():
        """Get all orders that are not completed or cancelled"""
        return ServiceOrder.query.filter(
            ServiceOrder.status.in_(['pending', 'in_progress'])
        ).order_by(ServiceOrder.created_at.asc()).all()

    @staticmethod
    def get_today_orders():
        """Get orders created today"""
        from sqlalchemy import and_, cast, Date
        today = datetime.utcnow().date()
        return ServiceOrder.query.filter(cast(ServiceOrder.created_at, Date) == today).all()

    @staticmethod
    def get_by_customer(customer_id, limit=10):
        """Get recent orders for a specific customer"""
        return ServiceOrder.query.filter_by(
            customer_id=customer_id
        ).order_by(ServiceOrder.created_at.desc()).limit(limit).all()

    def __repr__(self):
        return f'<ServiceOrder {self.order_number} ({self.status})>'