from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_, cast, Date
from app import db
from app.models import ServiceOrder, OrderService, Payment, User, Customer, Vehicle, Service

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Home page - redirect to dashboard or login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with real-time statistics"""
    # Get today's statistics
    today = datetime.utcnow().date()

    # Today's orders
    today_orders = ServiceOrder.query.filter(cast(ServiceOrder.created_at, Date) == today).all()
    today_completed = ServiceOrder.query.filter(
        and_(
            cast(ServiceOrder.completed_at, Date) == today,
            ServiceOrder.status == 'completed'
        )
    ).all()

    # Today's revenue
    today_revenue = db.session.query(func.sum(Payment.amount)).filter(
        cast(Payment.created_at, Date) == today
    ).scalar() or 0

    # Active queue
    active_orders = ServiceOrder.query.filter(
        ServiceOrder.status.in_(['pending', 'in_progress'])
    ).order_by(ServiceOrder.created_at.asc()).all()

    # Staff workload
    staff_workload = db.session.query(
        User.id,
        User.full_name,
        func.count(OrderService.id).label('active_services')
    ).join(OrderService).filter(
        and_(
            OrderService.status == 'in_progress',
            OrderService.assigned_staff_id == User.id
        )
    ).group_by(User.id, User.full_name).all()

    # Popular services today
    popular_services = db.session.query(
        Service.name,
        func.count(OrderService.id).label('count')
    ).join(OrderService).join(ServiceOrder).filter(
        and_(
            cast(ServiceOrder.created_at, Date) == today,
            OrderService.status == 'completed'
        )
    ).group_by(Service.id, Service.name).order_by(
        func.count(OrderService.id).desc()
    ).limit(5).all()

    # Recent payments
    recent_payments = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()

    stats = {
        'today_orders': len(today_orders),
        'today_completed': len(today_completed),
        'today_revenue': float(today_revenue),
        'active_queue_length': len(active_orders),
        'active_orders': active_orders,
        'staff_workload': staff_workload,
        'popular_services': popular_services,
        'recent_payments': recent_payments
    }

    # Add role-specific data
    if current_user.role == 'staff':
        # Staff can only see their assigned services
        my_active_services = OrderService.query.filter_by(
            assigned_staff_id=current_user.id,
            status='in_progress'
        ).all()
        stats['my_active_services'] = my_active_services

    elif current_user.role == 'manager':
        # Managers get additional insights
        peak_hour_data = db.session.query(
            func.extract('hour', ServiceOrder.created_at).label('hour'),
            func.count(ServiceOrder.id).label('count')
        ).filter(cast(ServiceOrder.created_at, Date) == today).group_by(
            func.extract('hour', ServiceOrder.created_at)
        ).order_by(func.count(ServiceOrder.id).desc()).first()

        stats['peak_hour'] = peak_hour_data[0] if peak_hour_data else None
        stats['peak_hour_count'] = peak_hour_data[1] if peak_hour_data else 0

    elif current_user.role == 'admin':
        # Admin gets system-wide data
        total_customers = Customer.query.count()
        total_vehicles = Vehicle.query.count()
        total_staff = User.query.filter_by(is_active=True).count()

        stats.update({
            'total_customers': total_customers,
            'total_vehicles': total_vehicles,
            'total_staff': total_staff
        })

    return render_template('dashboard.html', stats=stats)

@bp.route('/queue')
@login_required
def queue():
    """Live queue view"""
    active_orders = ServiceOrder.query.filter(
        ServiceOrder.status.in_(['pending', 'in_progress'])
    ).order_by(ServiceOrder.created_at.asc()).all()

    return render_template('queue.html', orders=active_orders, now=datetime.now())
    
@bp.route('/new-order')
@login_required
def new_order():
    """Create new service order form"""
    services = Service.query.filter_by(is_active=True).order_by(Service.display_order, Service.name).all()

    return render_template('orders/new.html', services=services)

@bp.route('/orders/<int:order_id>')
@login_required
def view_order(order_id):
    """View specific order details"""
    order = ServiceOrder.query.get_or_404(order_id)

    # Check permissions - staff can only see their assigned orders
    if current_user.role == 'staff':
        assigned_services = OrderService.query.filter_by(
            order_id=order_id,
            assigned_staff_id=current_user.id
        ).first()

        if not assigned_services and order.created_by != current_user.id:
            flash('You do not have permission to view this order', 'error')
            return redirect(url_for('main.dashboard'))

    return render_template('orders/view.html', order=order)

@bp.route('/customers')
@login_required
def customers():
    """Customer management page"""
    search = request.args.get('search', '').strip()

    if search:
        # Search by phone number or name
        customers = Customer.query.filter(
            or_(
                Customer.phone_number.like(f'%{search}%'),
                Customer.name.like(f'%{search}%')
            )
        ).order_by(Customer.updated_at.desc()).all()
    else:
        customers = Customer.query.order_by(Customer.updated_at.desc()).limit(50).all()

    return render_template('customers/index.html', customers=customers, search=search)

@bp.route('/customers/<int:customer_id>')
@login_required
def view_customer(customer_id):
    """View customer details and history"""
    customer = Customer.query.get_or_404(customer_id)

    # Get customer's orders
    orders = ServiceOrder.query.filter_by(customer_id=customer_id).order_by(
        ServiceOrder.created_at.desc()
    ).limit(20).all()

    # Get customer's vehicles
    vehicles = Vehicle.query.filter_by(customer_id=customer_id).all()

    return render_template('customers/view.html', customer=customer, orders=orders, vehicles=vehicles)

@bp.route('/vehicles')
@login_required
def vehicles():
    """Vehicle management page"""
    search = request.args.get('search', '').strip()

    if search:
        vehicles = Vehicle.query.filter(
            Vehicle.registration_number.like(f'%{search}%')
        ).order_by(Vehicle.created_at.desc()).all()
    else:
        vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).limit(50).all()

    return render_template('vehicles/index.html', vehicles=vehicles, search=search)

@bp.route('/services')
@login_required
def services():
    """Service management page"""
    services = Service.query.order_by(Service.display_order, Service.name).all()

    return render_template('services/index.html', services=services)

@bp.route('/payments')
@login_required
def payments():
    """Payment recording page"""
    search = request.args.get('search', '').strip()

    if search:
        payments = Payment.query.join(ServiceOrder).filter(
            ServiceOrder.order_number.like(f'%{search}%')
        ).order_by(Payment.created_at.desc()).all()
    else:
        payments = Payment.query.order_by(Payment.created_at.desc()).limit(50).all()

    return render_template('payments/index.html', payments=payments, search=search)

@bp.route('/reports')
@login_required
def reports():
    """Reports page"""
    # Default to today's report
    report_date = request.args.get('date', datetime.utcnow().strftime('%Y-%m-%d'))

    try:
        report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
    except ValueError:
        report_date = datetime.utcnow().date()

    # Get daily summary data
    from app.models.payment import Payment
    daily_summary = Payment.get_daily_summary(report_date)

    # Get daily orders
    daily_orders = ServiceOrder.query.filter(cast(ServiceOrder.created_at, Date) == report_date).all()

    # Get staff performance for the day
    staff_performance = []
    if current_user.role in ['manager', 'admin']:
        staff_performance = db.session.query(
            User.id,
            User.full_name,
            func.count(OrderService.id).label('completed_services'),
            func.sum(OrderService.price_charged).label('revenue_generated')
        ).join(OrderService).filter(
            and_(
                cast(OrderService.completed_at, Date) == report_date,
                OrderService.status == 'completed',
                OrderService.assigned_staff_id == User.id
            )
        ).group_by(User.id, User.full_name).all()

    return render_template('reports/index.html',
                         daily_summary=daily_summary,
                         daily_orders=daily_orders,
                         staff_performance=staff_performance,
                         report_date=report_date)

@bp.route('/staff')
@login_required
def staff():
    """Staff management page (admin/manager only)"""
    if current_user.role not in ['admin', 'manager']:
        flash('Admin or Manager access required', 'error')
        return redirect(url_for('main.dashboard'))

    staff = User.query.filter_by(is_active=True).order_by(User.role, User.full_name).all()

    return render_template('staff/index.html', staff=staff)

@bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Redirect to auth profile for consistency
    return redirect(url_for('auth.profile'))

@bp.route('/settings')
@login_required
def settings():
    """Settings page (admin only)"""
    if current_user.role != 'admin':
        flash('Admin access required', 'error')
        return redirect(url_for('main.dashboard'))

    return render_template('settings.html')

# Helper routes for AJAX requests
@bp.route('/api/dashboard-stats')
@login_required
def dashboard_stats():
    """Get dashboard statistics for AJAX updates"""
    today = datetime.utcnow().date()

    # Quick stats calculation
    active_count = ServiceOrder.query.filter(
        ServiceOrder.status.in_(['pending', 'in_progress'])
    ).count()

    today_revenue = db.session.query(func.sum(Payment.amount)).filter(
        cast(Payment.created_at, Date) == today
    ).scalar() or 0

    today_orders = ServiceOrder.query.filter(cast(ServiceOrder.created_at, Date) == today).count()

    from flask import jsonify
    return jsonify({
        'active_queue': active_count,
        'today_revenue': float(today_revenue),
        'today_orders': today_orders,
        'last_updated': datetime.utcnow().isoformat()
    })

# Error handlers for template pages
@bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@bp.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500