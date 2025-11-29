from datetime import datetime
from app import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('service_orders.id'), nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('cash', 'mpesa', 'airtel', 'card', name='payment_method'),
                                nullable=False)
    transaction_reference = db.Column(db.String(100), nullable=True)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)

    def __init__(self, order_id, amount, payment_method, recorded_by, transaction_ref=None, notes=None):
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.recorded_by = recorded_by
        self.transaction_reference = transaction_ref
        self.notes = notes

    @staticmethod
    def get_payment_method_display(payment_method):
        """Get display name for payment method"""
        display_names = {
            'cash': 'Cash',
            'mpesa': 'M-Pesa',
            'airtel': 'Airtel Money',
            'card': 'Card'
        }
        return display_names.get(payment_method, payment_method.title())

    def get_payment_method_display_name(self):
        """Get display name for this payment's method"""
        return self.get_payment_method_display(self.payment_method)

    def get_receipt_details(self):
        """Get formatted receipt details"""
        order = self.order
        details = {
            'payment_id': self.id,
            'payment_method': self.get_payment_method_display_name(),
            'amount': float(self.amount),
            'transaction_reference': self.transaction_reference,
            'paid_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'recorded_by': self.recorder.full_name if self.recorder else None
        }

        if order:
            details.update({
                'order_number': order.order_number,
                'customer_name': order.customer.name if order.customer else 'Walk-in Customer',
                'customer_phone': order.customer.phone_number if order.customer else None,
                'vehicle_registration': order.vehicle.registration_number if order.vehicle else None,
                'vehicle_info': f"{order.vehicle.make} {order.vehicle.model}" if order.vehicle and order.vehicle.make else 'Unknown Vehicle',
                'total_order_amount': float(order.total_amount),
                'balance_due': order.get_balance_due(),
                'payment_status': order.payment_status
            })

        return details

    def is_full_payment(self):
        """Check if this payment covers the entire order"""
        if not self.order:
            return False
        return float(self.amount) >= float(self.order.total_amount)

    def get_change_amount(self):
        """Calculate change for cash payments"""
        if self.payment_method != 'cash' or not self.order:
            return 0
        return max(0, float(self.amount) - float(self.order.total_amount))

    def validate_amount(self):
        """Validate payment amount against order total"""
        if not self.order:
            return False, "Order not found"

        order_total = float(self.order.total_amount)
        amount_paid = float(self.amount)
        current_paid = float(self.order.amount_paid) - float(self.amount)  # Subtract current payment to get previous total

        if amount_paid <= 0:
            return False, "Payment amount must be greater than 0"

        if (current_paid + amount_paid) > (order_total * 1.5):  # Allow overpayment up to 150% of order total
            return False, f"Payment amount exceeds order total by too much"

        return True, "Valid payment amount"

    def process_payment(self):
        """Process payment and update order"""
        is_valid, message = self.validate_amount()
        if not is_valid:
            return False, message

        if self.order:
            # Update order payment status
            self.order.amount_paid += float(self.amount)
            self.order.update_payment_status()
            db.session.commit()
            return True, "Payment processed successfully"

        return False, "Order not found"

    def refund_payment(self, reason=None, refund_amount=None):
        """Process refund (mark as refunded - doesn't actually return money)"""
        refund_amount = refund_amount or self.amount
        refund_amount = min(float(refund_amount), float(self.amount))

        if not self.order:
            return False, "Order not found"

        # Update order amount paid
        self.order.amount_paid = max(0, float(self.order.amount_paid) - refund_amount)
        self.order.update_payment_status()

        # Add refund note
        refund_note = f"Refunded KES {refund_amount:.2f}"
        if reason:
            refund_note += f" - {reason}"

        if self.notes:
            self.notes = f"{self.notes}\n[REFUNDED {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] {refund_note}"
        else:
            self.notes = f"[REFUNDED {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] {refund_note}"

        db.session.commit()
        return True, "Refund processed successfully"

    @staticmethod
    def get_daily_summary(date=None):
        """Get payment summary for a specific date"""
        if date is None:
            date = datetime.utcnow().date()

        from sqlalchemy import and_, func, cast, Date

        # Total payments by method
        payment_summary = db.session.query(
            Payment.payment_method,
            func.count(Payment.id).label('count'),
            func.sum(Payment.amount).label('total')
        ).filter(cast(Payment.created_at, Date) == date).group_by(Payment.payment_method).all()

        # Total payments for the day
        daily_total = db.session.query(func.sum(Payment.amount)).filter(
            cast(Payment.created_at, Date) == date
        ).scalar() or 0

        return {
            'date': date.isoformat(),
            'total_collected': float(daily_total),
            'by_method': [
                {
                    'method': method,
                    'method_display': Payment.get_payment_method_display(method),
                    'count': count,
                    'total': float(total)
                }
                for method, count, total in payment_summary
            ],
            'payment_count': sum([count for _, count, _ in payment_summary])
        }

    @staticmethod
    def get_weekly_summary(year=None, week=None):
        """Get payment summary for a specific week"""
        if year is None:
            year = datetime.utcnow().year
        if week is None:
            week = datetime.utcnow().isocalendar()[1]

        from sqlalchemy import and_, func, extract

        weekly_total = db.session.query(func.sum(Payment.amount)).filter(
            and_(
                extract('year', Payment.created_at) == year,
                extract('week', Payment.created_at) == week
            )
        ).scalar() or 0

        return {
            'year': year,
            'week': week,
            'total_collected': float(weekly_total)
        }

    @staticmethod
    def get_monthly_summary(year=None, month=None):
        """Get payment summary for a specific month"""
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month

        from sqlalchemy import and_, func, extract

        monthly_total = db.session.query(func.sum(Payment.amount)).filter(
            and_(
                extract('year', Payment.created_at) == year,
                extract('month', Payment.created_at) == month
            )
        ).scalar() or 0

        return {
            'year': year,
            'month': month,
            'total_collected': float(monthly_total)
        }

    @staticmethod
    def get_payment_trends(days=30):
        """Get payment trends over last N days"""
        from sqlalchemy import and_, func, cast, Date
        from datetime import timedelta

        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days-1)

        daily_payments = db.session.query(
            cast(Payment.created_at, Date).label('date'),
            func.count(Payment.id).label('count'),
            func.sum(Payment.amount).label('total')
        ).filter(
            and_(
                cast(Payment.created_at, Date) >= start_date,
                cast(Payment.created_at, Date) <= end_date
            )
        ).group_by(cast(Payment.created_at, Date)).order_by('date').all()

        return [
            {
                'date': date.isoformat(),
                'payment_count': count,
                'total_collected': float(total)
            }
            for date, count, total in daily_payments
        ]

    def to_dict(self, include_receipt_details=False):
        """Convert to dictionary for API responses"""
        result = {
            'id': self.id,
            'order_id': self.order_id,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'payment_method_display': self.get_payment_method_display_name(),
            'transaction_reference': self.transaction_reference,
            'recorded_by': self.recorded_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes': self.notes
        }

        if include_receipt_details:
            result.update(self.get_receipt_details())

        return result

    @staticmethod
    def get_recent_payments(limit=20):
        """Get recent payments"""
        return Payment.query.order_by(Payment.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_by_transaction_reference(reference):
        """Find payment by transaction reference"""
        return Payment.query.filter_by(transaction_reference=reference).first()

    def __repr__(self):
        return f'<Payment KES {self.amount} via {self.payment_method} for Order {self.order_id}>'