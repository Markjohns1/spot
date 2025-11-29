from datetime import datetime
from app import db

class OrderService(db.Model):
    __tablename__ = 'order_services'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False, index=True)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    price_charged = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', name='order_service_status'),
                       default='pending', nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    staff_assignments = db.relationship('StaffAssignment', backref='order_service', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, order_id, service_id, price_charged, assigned_staff_id=None):
        self.order_id = order_id
        self.service_id = service_id
        self.price_charged = price_charged
        self.assigned_staff_id = assigned_staff_id

    def assign_staff(self, staff_id, role='primary'):
        """Assign staff member to this service"""
        from .staff_assignment import StaffAssignment
        from .user import User

        # Verify staff exists and is active
        staff = User.query.filter_by(id=staff_id, is_active=True).first()
        if not staff:
            return False

        self.assigned_staff_id = staff_id

        # Create staff assignment record
        assignment = StaffAssignment(
            order_service_id=self.id,
            staff_id=staff_id,
            role=role
        )
        db.session.add(assignment)

        # Start service if this is the first assignment
        if self.status == 'pending':
            self.start_service()

        db.session.commit()
        return True

    def start_service(self):
        """Mark service as in progress"""
        if self.status == 'pending' and self.assigned_staff_id:
            self.status = 'in_progress'
            self.started_at = datetime.utcnow()
            db.session.commit()
            return True
        return False

    def complete_service(self):
        """Mark service as completed"""
        if self.status in ['pending', 'in_progress']:
            self.status = 'completed'
            self.completed_at = datetime.utcnow()

            # Check if this completes the entire order
            order = self.order
            if order:
                order.complete_service()

            db.session.commit()
            return True
        return False

    def get_duration(self):
        """Calculate service duration"""
        if self.started_at:
            end_time = self.completed_at or datetime.utcnow()
            return end_time - self.started_at
        return None

    def get_duration_minutes(self):
        """Get duration in minutes"""
        duration = self.get_duration()
        if duration:
            return int(duration.total_seconds() / 60)
        return None

    def is_overdue(self, max_minutes=None):
        """Check if service is taking longer than expected"""
        if not self.started_at or self.completed_at:
            return False

        if max_minutes is None:
            max_minutes = self.service.duration_minutes if self.service else 60

        duration = datetime.utcnow() - self.started_at
        return duration.total_seconds() > (max_minutes * 60)

    def get_assigned_staff_names(self):
        """Get names of all assigned staff"""
        names = []
        if self.assigned_staff:
            names.append(self.assigned_staff.full_name)

        # Get additional staff from assignments
        for assignment in self.staff_assignments:
            if assignment.staff and assignment.staff.full_name not in names:
                names.append(assignment.staff.full_name)

        return names

    def add_note(self, note):
        """Add note to service"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        if self.notes:
            self.notes = f"{self.notes}\n[{timestamp}] {note}"
        else:
            self.notes = f"[{timestamp}] {note}"
        db.session.commit()

    def update_price(self, new_price, reason=None):
        """Update price charged for this service"""
        old_price = self.price_charged
        self.price_charged = new_price

        # Add note about price change
        if reason:
            self.add_note(f"Price changed from KES {old_price} to KES {new_price}: {reason}")
        else:
            self.add_note(f"Price changed from KES {old_price} to KES {new_price}")

        # Update order total
        if self.order:
            self.order.calculate_total()

        db.session.commit()

    def can_be_cancelled(self):
        """Check if service can be cancelled"""
        return self.status in ['pending', 'in_progress']

    def cancel_service(self, reason=None):
        """Cancel this service"""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            if reason:
                self.add_note(f"Service cancelled: {reason}")
            else:
                self.add_note("Service cancelled")

            # Check if entire order should be cancelled
            if self.order:
                remaining_services = self.order.order_services.filter(
                    OrderService.status.in_(['pending', 'in_progress'])
                ).count()

                if remaining_services == 0:
                    self.order.cancel_service("All services cancelled")

            db.session.commit()
            return True
        return False

    def get_service_efficiency(self):
        """Calculate how efficient the service was compared to expected duration"""
        if not self.started_at or not self.completed_at or not self.service:
            return None

        actual_duration = self.get_duration_minutes()
        expected_duration = self.service.duration_minutes

        if expected_duration > 0:
            efficiency = (expected_duration / actual_duration) * 100 if actual_duration > 0 else 100
            return min(max(efficiency, 0), 200)  # Cap between 0-200%
        return None

    def to_dict(self, include_details=False):
        """Convert to dictionary for API responses"""
        result = {
            'id': self.id,
            'order_id': self.order_id,
            'service_id': self.service_id,
            'assigned_staff_id': self.assigned_staff_id,
            'price_charged': float(self.price_charged),
            'status': self.status,
            'notes': self.notes,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration_minutes': self.get_duration_minutes(),
            'is_overdue': self.is_overdue(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_details:
            result.update({
                'service': self.service.to_dict() if self.service else None,
                'assigned_staff': self.assigned_staff.to_dict() if self.assigned_staff else None,
                'assigned_staff_names': self.get_assigned_staff_names(),
                'all_assigned_staff': [assignment.to_dict() for assignment in self.staff_assignments],
                'efficiency': self.get_service_efficiency()
            })

        return result

    @staticmethod
    def get_active_services():
        """Get all services currently in progress"""
        return OrderService.query.filter_by(status='in_progress').order_by(OrderService.started_at.asc()).all()

    @staticmethod
    def get_staff_active_services(staff_id):
        """Get active services for specific staff member"""
        return OrderService.query.filter_by(
            assigned_staff_id=staff_id,
            status='in_progress'
        ).order_by(OrderService.started_at.asc()).all()

    @staticmethod
    def get_completed_services_today():
        """Get services completed today"""
        from sqlalchemy import and_, cast, Date
        today = datetime.utcnow().date()
        return OrderService.query.filter(
            and_(
                OrderService.status == 'completed',
                cast(OrderService.completed_at, Date) == today
            )
        ).all()

    @staticmethod
    def get_overdue_services():
        """Get services that are taking longer than expected"""
        overdue_services = []
        for service in OrderService.query.filter_by(status='in_progress').all():
            if service.is_overdue():
                overdue_services.append(service)
        return overdue_services

    def __repr__(self):
        service_name = self.service.name if self.service else 'Unknown'
        return f'<OrderService {service_name} ({self.status})>'