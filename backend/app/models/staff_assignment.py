from datetime import datetime
from app import db

class StaffAssignment(db.Model):
    __tablename__ = 'staff_assignments'

    id = db.Column(db.Integer, primary_key=True)
    order_service_id = db.Column(db.Integer, db.ForeignKey('order_services.id'), nullable=False, index=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    role = db.Column(db.Enum('primary', 'assistant', name='assignment_role'),
                     default='primary', nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, order_service_id, staff_id, role='primary'):
        self.order_service_id = order_service_id
        self.staff_id = staff_id
        self.role = role

    @staticmethod
    def assign_staff_to_service(order_service_id, staff_id, role='primary'):
        """Assign staff member to a service"""
        from .user import User
        from .order_service import OrderService

        # Verify staff exists and is active
        staff = User.query.filter_by(id=staff_id, is_active=True).first()
        if not staff:
            return False, "Staff member not found or inactive"

        # Verify service exists
        service = OrderService.query.get(order_service_id)
        if not service:
            return False, "Service not found"

        # Check if staff is already assigned to this service
        existing = StaffAssignment.query.filter_by(
            order_service_id=order_service_id,
            staff_id=staff_id
        ).first()

        if existing:
            return False, "Staff already assigned to this service"

        # Create assignment
        assignment = StaffAssignment(order_service_id, staff_id, role)
        db.session.add(assignment)

        # Update primary staff assignment if this is primary
        if role == 'primary':
            service.assigned_staff_id = staff_id
            if service.status == 'pending':
                service.start_service()

        db.session.commit()
        return True, "Staff assigned successfully"

    @staticmethod
    def remove_staff_from_service(order_service_id, staff_id):
        """Remove staff member from a service"""
        from .order_service import OrderService

        # Find assignment
        assignment = StaffAssignment.query.filter_by(
            order_service_id=order_service_id,
            staff_id=staff_id
        ).first()

        if not assignment:
            return False, "Assignment not found"

        service = OrderService.query.get(order_service_id)
        if service:
            # If removing primary staff, reassign if possible
            if assignment.role == 'primary':
                other_assignments = StaffAssignment.query.filter_by(
                    order_service_id=order_service_id
                ).filter(StaffAssignment.id != assignment.id).all()

                if other_assignments:
                    # Promote first assistant to primary
                    new_primary = other_assignments[0]
                    new_primary.role = 'primary'
                    service.assigned_staff_id = new_primary.staff_id
                else:
                    # No other staff, clear assignment
                    service.assigned_staff_id = None

        db.session.delete(assignment)
        db.session.commit()
        return True, "Staff removed from service"

    @staticmethod
    def get_service_assignments(order_service_id):
        """Get all staff assignments for a service"""
        return StaffAssignment.query.filter_by(order_service_id=order_service_id).all()

    @staticmethod
    def get_staff_active_assignments(staff_id):
        """Get active assignments for staff member"""
        from sqlalchemy import and_
        from .order_service import OrderService

        return db.session.query(StaffAssignment).join(OrderService).filter(
            and_(
                StaffAssignment.staff_id == staff_id,
                OrderService.status.in_(['pending', 'in_progress'])
            )
        ).all()

    @staticmethod
    def get_staff_completed_assignments_today(staff_id):
        """Get assignments completed today for staff member"""
        from sqlalchemy import and_, cast, Date
        from .order_service import OrderService

        today = datetime.utcnow().date()
        return db.session.query(StaffAssignment).join(OrderService).filter(
            and_(
                StaffAssignment.staff_id == staff_id,
                OrderService.status == 'completed',
                cast(OrderService.completed_at, Date) == today
            )
        ).all()

    @staticmethod
    def reassign_service(order_service_id, old_staff_id, new_staff_id):
        """Reassign service from one staff member to another"""
        from .user import User

        # Verify new staff exists and is active
        new_staff = User.query.filter_by(id=new_staff_id, is_active=True).first()
        if not new_staff:
            return False, "New staff member not found or inactive"

        # Find existing assignment
        assignment = StaffAssignment.query.filter_by(
            order_service_id=order_service_id,
            staff_id=old_staff_id
        ).first()

        if not assignment:
            return False, "Existing assignment not found"

        # Check if new staff is already assigned
        existing_new = StaffAssignment.query.filter_by(
            order_service_id=order_service_id,
            staff_id=new_staff_id
        ).first()

        if existing_new:
            return False, "New staff member already assigned to this service"

        # Update assignment
        assignment.staff_id = new_staff_id

        # Update order service if this was primary
        if assignment.role == 'primary':
            from .order_service import OrderService
            service = OrderService.query.get(order_service_id)
            if service:
                service.assigned_staff_id = new_staff_id

        db.session.commit()
        return True, "Service reassigned successfully"

    @staticmethod
    def get_staff_workload_distribution(date=None):
        """Get workload distribution among staff for a specific date"""
        if date is None:
            date = datetime.utcnow().date()

        from sqlalchemy import func, and_, cast, Date
        from .order_service import OrderService

        # Count active assignments per staff
        workload = db.session.query(
            User.id,
            User.full_name,
            func.count(StaffAssignment.id).label('active_assignments'),
            func.sum(func.case([(OrderService.status == 'completed', 1)], else_=0)).label('completed_today')
        ).join(User).join(OrderService).filter(
            and_(
                cast(OrderService.started_at, Date) == date,
                OrderService.status.in_(['in_progress', 'completed'])
            )
        ).group_by(User.id, User.full_name).all()

        return [
            {
                'staff_id': staff_id,
                'staff_name': full_name,
                'active_assignments': active_assignments or 0,
                'completed_today': completed_today or 0
            }
            for staff_id, full_name, active_assignments, completed_today in workload
        ]

    @staticmethod
    def get_staff_efficiency_report(staff_id, days=30):
        """Get efficiency report for staff member"""
        from datetime import timedelta
        from sqlalchemy import and_, cast, Date
        from .order_service import OrderService

        start_date = datetime.utcnow().date() - timedelta(days=days-1)

        # Get all assignments in period
        assignments = db.session.query(StaffAssignment).join(OrderService).filter(
            and_(
                StaffAssignment.staff_id == staff_id,
                cast(OrderService.completed_at, Date) >= start_date,
                OrderService.status == 'completed'
            )
        ).all()

        # Calculate efficiency metrics
        total_services = len(assignments)
        total_efficiency = 0
        efficiency_count = 0

        for assignment in assignments:
            if assignment.order_service:
                efficiency = assignment.order_service.get_service_efficiency()
                if efficiency is not None:
                    total_efficiency += efficiency
                    efficiency_count += 1

        avg_efficiency = total_efficiency / efficiency_count if efficiency_count > 0 else 0

        return {
            'staff_id': staff_id,
            'period_days': days,
            'total_completed': total_services,
            'average_efficiency': round(avg_efficiency, 2),
            'services_with_efficiency_data': efficiency_count,
            'efficiency_percentage': round(efficiency_count / total_services * 100, 2) if total_services > 0 else 0
        }

    def get_assignment_duration(self):
        """Calculate how long staff has been assigned"""
        from datetime import datetime

        end_time = datetime.utcnow()
        if self.order_service and self.order_service.completed_at:
            end_time = self.order_service.completed_at

        return end_time - self.assigned_at

    def get_assignment_duration_minutes(self):
        """Get assignment duration in minutes"""
        duration = self.get_assignment_duration()
        if duration:
            return int(duration.total_seconds() / 60)
        return None

    def to_dict(self, include_details=False):
        """Convert to dictionary for API responses"""
        result = {
            'id': self.id,
            'order_service_id': self.order_service_id,
            'staff_id': self.staff_id,
            'role': self.role,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'duration_minutes': self.get_assignment_duration_minutes()
        }

        if include_details:
            result.update({
                'staff': self.staff.to_dict() if self.staff else None,
                'order_service': self.order_service.to_dict(include_details=True) if self.order_service else None
            })

        return result

    @staticmethod
    def get_active_assignments():
        """Get all currently active staff assignments"""
        from sqlalchemy import and_
        from .order_service import OrderService

        return db.session.query(StaffAssignment).join(OrderService).filter(
            OrderService.status.in_(['pending', 'in_progress'])
        ).all()

    def __repr__(self):
        staff_name = self.staff.full_name if self.staff else 'Unknown'
        service_name = self.order_service.service.name if self.order_service and self.order_service.service else 'Unknown'
        return f'<StaffAssignment {staff_name} -> {service_name} ({self.role})>'