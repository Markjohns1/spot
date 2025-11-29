from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_, cast, Date
from app import db
from app.models import *
from app.routes.auth import staff_required, manager_required, admin_required

bp = Blueprint('api', __name__, url_prefix='/api')

# ==================== AUTHENTICATION ENDPOINTS ====================

@bp.route('/auth/login', methods=['POST'])
def api_login():
    """API login endpoint"""
    # Handled by auth blueprint
    pass

@bp.route('/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """API logout endpoint"""
    # Handled by auth blueprint
    pass

@bp.route('/auth/profile', methods=['GET'])
@login_required
def api_profile():
    """Get current user profile"""
    return jsonify({
        'success': True,
        'data': {
            'user': current_user.to_dict()
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/auth/change-password', methods=['POST'])
@login_required
def api_change_password():
    """Change password via API"""
    # Handled by auth blueprint
    pass

# ==================== CUSTOMER ENDPOINTS ====================

@bp.route('/customers', methods=['GET'])
@login_required
def get_customers():
    """Get customers with optional search and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()

    query = Customer.query

    if search:
        query = query.filter(
            or_(
                Customer.phone_number.like(f'%{search}%'),
                Customer.name.like(f'%{search}%'),
                Customer.email.like(f'%{search}%')
            )
        )

    customers = query.order_by(Customer.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'data': {
            'customers': [customer.to_dict() for customer in customers.items],
            'pagination': {
                'page': customers.page,
                'pages': customers.pages,
                'per_page': customers.per_page,
                'total': customers.total,
                'has_next': customers.has_next,
                'has_prev': customers.has_prev
            }
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/customers', methods=['POST'])
@login_required
def create_customer():
    """Create new customer"""
    data = request.get_json()

    # Validate required fields
    if not data.get('phone_number'):
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Phone number is required'
            }
        }), 400

    # Check for existing customer
    existing = Customer.query.filter_by(phone_number=data['phone_number']).first()
    if existing:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': 'Customer with this phone number already exists'
            }
        }), 400

    # Create customer
    customer = Customer(
        phone_number=data['phone_number'],
        name=data.get('name'),
        email=data.get('email')
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'customer': customer.to_dict()
        },
        'message': 'Customer created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@bp.route('/customers/<int:customer_id>', methods=['GET'])
@login_required
def get_customer(customer_id):
    """Get specific customer details"""
    customer = Customer.query.get_or_404(customer_id)

    return jsonify({
        'success': True,
        'data': {
            'customer': customer.to_dict(),
            'vehicles': [vehicle.to_dict() for vehicle in customer.vehicles.all()],
            'recent_orders': [order.to_dict() for order in customer.get_service_history(10)]
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/customers/<int:customer_id>', methods=['PUT'])
@login_required
def update_customer(customer_id):
    """Update customer information"""
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()

    # Update fields
    if 'name' in data:
        customer.name = data['name']
    if 'email' in data:
        customer.email = data['email']
    if 'phone_number' in data and data['phone_number'] != customer.phone_number:
        # Check for duplicate
        existing = Customer.query.filter_by(phone_number=data['phone_number']).first()
        if existing:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'DUPLICATE_ERROR',
                    'message': 'Phone number already exists'
                }
            }), 400
        customer.phone_number = data['phone_number']

    customer.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'customer': customer.to_dict()
        },
        'message': 'Customer updated successfully',
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== VEHICLE ENDPOINTS ====================

@bp.route('/vehicles', methods=['GET'])
@login_required
def get_vehicles():
    """Get vehicles with optional search"""
    search = request.args.get('search', '').strip()
    customer_id = request.args.get('customer_id', type=int)

    query = Vehicle.query

    if search:
        query = query.filter(
            or_(
                Vehicle.registration_number.like(f'%{search}%'),
                Vehicle.make.like(f'%{search}%'),
                Vehicle.model.like(f'%{search}%')
            )
        )

    if customer_id:
        query = query.filter_by(customer_id=customer_id)

    vehicles = query.order_by(Vehicle.created_at.desc()).all()

    return jsonify({
        'success': True,
        'data': {
            'vehicles': [vehicle.to_dict() for vehicle in vehicles]
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/vehicles', methods=['POST'])
@login_required
def create_vehicle():
    """Create new vehicle"""
    data = request.get_json()

    # Validate required fields
    if not data.get('customer_id') or not data.get('registration_number'):
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Customer ID and registration number are required'
            }
        }), 400

    # Validate registration number
    if not Vehicle.validate_registration(data['registration_number']):
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Invalid registration number format'
            }
        }), 400

    # Check for existing registration
    existing = Vehicle.query.filter_by(registration_number=Vehicle.normalize_registration(data['registration_number'])).first()
    if existing:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': 'Vehicle with this registration number already exists'
            }
        }), 400

    # Create vehicle
    vehicle = Vehicle(
        customer_id=data['customer_id'],
        registration_number=data['registration_number'],
        make=data.get('make'),
        model=data.get('model'),
        color=data.get('color')
    )

    db.session.add(vehicle)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'vehicle': vehicle.to_dict()
        },
        'message': 'Vehicle created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@bp.route('/vehicles/<int:vehicle_id>', methods=['GET'])
@login_required
def get_vehicle(vehicle_id):
    """Get specific vehicle details"""
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    return jsonify({
        'success': True,
        'data': {
            'vehicle': vehicle.to_dict(),
            'customer': vehicle.customer.to_dict() if vehicle.customer else None,
            'service_history': [order.to_dict() for order in vehicle.get_service_history(10)]
        },
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== SERVICE ENDPOINTS ====================

@bp.route('/services', methods=['GET'])
@login_required
def get_services():
    """Get all active services"""
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'
    include_stats = request.args.get('include_stats', 'false').lower() == 'true'

    query = Service.query
    if not include_inactive:
        query = query.filter_by(is_active=True)

    services = query.order_by(Service.display_order, Service.name).all()

    return jsonify({
        'success': True,
        'data': {
            'services': [service.to_dict(include_stats) for service in services]
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/services', methods=['POST'])
@login_required
@admin_required
def create_service():
    """Create new service (admin only)"""
    data = request.get_json()

    # Validate required fields
    if not data.get('name') or not data.get('base_price'):
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Service name and base price are required'
            }
        }), 400

    # Check for existing service
    existing = Service.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': 'Service with this name already exists'
            }
        }), 400

    # Create service
    service = Service(
        name=data['name'],
        base_price=data['base_price'],
        duration_minutes=data.get('duration_minutes', 30),
        description=data.get('description'),
        display_order=data.get('display_order', 0)
    )

    db.session.add(service)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'service': service.to_dict()
        },
        'message': 'Service created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@bp.route('/services/<int:service_id>', methods=['PUT'])
@login_required
@admin_required
def update_service(service_id):
    """Update service (admin only)"""
    service = Service.query.get_or_404(service_id)
    data = request.get_json()

    # Update fields
    if 'name' in data:
        service.name = data['name']
    if 'base_price' in data:
        service.base_price = data['base_price']
    if 'duration_minutes' in data:
        service.duration_minutes = data['duration_minutes']
    if 'description' in data:
        service.description = data['description']
    if 'display_order' in data:
        service.display_order = data['display_order']
    if 'is_active' in data:
        service.is_active = data['is_active']

    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'service': service.to_dict()
        },
        'message': 'Service updated successfully',
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== ORDER ENDPOINTS ====================

@bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    """Get orders with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    customer_id = request.args.get('customer_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    query = ServiceOrder.query

    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if customer_id:
        query = query.filter_by(customer_id=customer_id)
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(cast(ServiceOrder.created_at, Date) >= date_from)
        except ValueError:
            pass
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(cast(ServiceOrder.created_at, Date) <= date_to)
        except ValueError:
            pass

    # Staff can only see their own orders or orders they're assigned to
    if current_user.role == 'staff':
        from sqlalchemy import or_
        query = query.filter(
            or_(
                ServiceOrder.created_by == current_user.id,
                ServiceOrder.id.in_(
                    db.session.query(OrderService.order_id).filter_by(
                        assigned_staff_id=current_user.id
                    )
                )
            )
        )

    orders = query.order_by(ServiceOrder.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'data': {
            'orders': [order.to_dict(include_details=True) for order in orders.items],
            'pagination': {
                'page': orders.page,
                'pages': orders.pages,
                'per_page': orders.per_page,
                'total': orders.total,
                'has_next': orders.has_next,
                'has_prev': orders.has_prev
            }
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/orders', methods=['POST'])
@login_required
def create_order():
    """Create new service order"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['customer_id', 'vehicle_id', 'services']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'{field.replace("_", " ").title()} is required'
                }
            }), 400

    # Validate services array
    if not isinstance(data['services'], list) or len(data['services']) == 0:
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'At least one service must be selected'
            }
        }), 400

    # Create order
    order_number = ServiceOrder.generate_order_number()
    order = ServiceOrder(
        order_number=order_number,
        customer_id=data['customer_id'],
        vehicle_id=data['vehicle_id'],
        created_by=current_user.id,
        notes=data.get('notes')
    )

    db.session.add(order)
    db.session.flush()  # Get order ID

    # Add services to order
    total_amount = 0
    for service_data in data['services']:
        service = Service.query.get(service_data['service_id'])
        if not service:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': f'Service with ID {service_data["service_id"]} not found'
                }
            }), 404

        price = service_data.get('price', service.base_price)

        order_service = OrderService(
            order_id=order.id,
            service_id=service.id,
            price_charged=price,
            assigned_staff_id=service_data.get('assigned_staff_id')
        )

        db.session.add(order_service)
        total_amount += price

    order.total_amount = total_amount
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'order': order.to_dict(include_details=True)
        },
        'message': 'Order created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@bp.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get specific order details"""
    order = ServiceOrder.query.get_or_404(order_id)

    # Check permissions for staff
    if current_user.role == 'staff':
        has_permission = (
            order.created_by == current_user.id or
            any(os.assigned_staff_id == current_user.id for os in order.order_services)
        )
        if not has_permission:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You do not have permission to view this order'
                }
            }), 403

    return jsonify({
        'success': True,
        'data': {
            'order': order.to_dict(include_details=True)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/orders/<int:order_id>/start', methods=['POST'])
@login_required
def start_order(order_id):
    """Start order processing"""
    order = ServiceOrder.query.get_or_404(order_id)

    # Check permissions
    if current_user.role == 'staff':
        has_permission = any(os.assigned_staff_id == current_user.id for os in order.order_services)
        if not has_permission:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You are not assigned to this order'
                }
            }), 403

    if order.start_service():
        return jsonify({
            'success': True,
            'message': 'Order started successfully',
            'timestamp': datetime.utcnow().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_STATE',
                'message': 'Order cannot be started'
            }
        }), 400

@bp.route('/orders/<int:order_id>/finish', methods=['POST'])
@login_required
def finish_order(order_id):
    """Complete order"""
    order = ServiceOrder.query.get_or_404(order_id)

    # Check permissions
    if current_user.role == 'staff':
        has_permission = any(os.assigned_staff_id == current_user.id for os in order.order_services)
        if not has_permission:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': 'You are not assigned to this order'
                }
            }), 403

    if order.complete_service():
        return jsonify({
            'success': True,
            'message': 'Order completed successfully',
            'timestamp': datetime.utcnow().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_STATE',
                'message': 'Order cannot be completed. Some services may still be in progress.'
            }
        }), 400

@bp.route('/orders/queue', methods=['GET'])
@login_required
def get_queue():
    """Get current active queue"""
    active_orders = ServiceOrder.query.filter(
        ServiceOrder.status.in_(['pending', 'in_progress'])
    ).order_by(ServiceOrder.created_at.asc()).all()

    return jsonify({
        'success': True,
        'data': {
            'queue': [order.to_dict(include_details=True) for order in active_orders],
            'queue_length': len(active_orders)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== PAYMENT ENDPOINTS ====================

@bp.route('/payments', methods=['GET'])
@login_required
def get_payments():
    """Get payments with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    payment_method = request.args.get('payment_method')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    query = Payment.query

    # Apply filters
    if payment_method:
        query = query.filter_by(payment_method=payment_method)
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(cast(Payment.created_at, Date) >= date_from)
        except ValueError:
            pass
    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(cast(Payment.created_at, Date) <= date_to)
        except ValueError:
            pass

    payments = query.order_by(Payment.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'success': True,
        'data': {
            'payments': [payment.to_dict(include_receipt_details=True) for payment in payments.items],
            'pagination': {
                'page': payments.page,
                'pages': payments.pages,
                'per_page': payments.per_page,
                'total': payments.total,
                'has_next': payments.has_next,
                'has_prev': payments.has_prev
            }
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/payments', methods=['POST'])
@login_required
def create_payment():
    """Record new payment"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['order_id', 'amount', 'payment_method']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'{field.replace("_", " ").title()} is required'
                }
            }), 400

    order = ServiceOrder.query.get(data['order_id'])
    if not order:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Order not found'
            }
        }), 404

    # Create payment
    payment = Payment(
        order_id=data['order_id'],
        amount=data['amount'],
        payment_method=data['payment_method'],
        recorded_by=current_user.id,
        transaction_reference=data.get('transaction_reference'),
        notes=data.get('notes')
    )

    db.session.add(payment)

    # Process payment
    success, message = payment.process_payment()
    if not success:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'PAYMENT_ERROR',
                'message': message
            }
        }), 400

    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'payment': payment.to_dict(include_receipt_details=True),
            'order': order.to_dict()
        },
        'message': 'Payment recorded successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@bp.route('/payments/daily', methods=['GET'])
@login_required
def get_daily_payments():
    """Get daily payment summary"""
    date = request.args.get('date')
    if date:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.utcnow().date()
    else:
        date = datetime.utcnow().date()

    summary = Payment.get_daily_summary(date)

    return jsonify({
        'success': True,
        'data': summary,
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/payments/<int:payment_id>/receipt', methods=['GET'])
@login_required
def get_payment_receipt(payment_id):
    """Generate payment receipt"""
    payment = Payment.query.get_or_404(payment_id)

    receipt_data = payment.get_receipt_details()

    return jsonify({
        'success': True,
        'data': {
            'receipt': receipt_data
        },
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== REPORTING ENDPOINTS ====================

@bp.route('/reports/daily', methods=['GET'])
@login_required
@manager_required
def get_daily_report():
    """Get daily operations report"""
    date = request.args.get('date')
    if date:
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            date = datetime.utcnow().date()
    else:
        date = datetime.utcnow().date()

    # Get daily metrics
    daily_orders = ServiceOrder.query.filter(cast(ServiceOrder.created_at, Date) == date).all()
    completed_orders = [order for order in daily_orders if order.status == 'completed']

    daily_revenue = db.session.query(func.sum(Payment.amount)).filter(
        cast(Payment.created_at, Date) == date
    ).scalar() or 0

    # Service breakdown
    service_breakdown = db.session.query(
        Service.name,
        func.count(OrderService.id).label('count'),
        func.sum(OrderService.price_charged).label('revenue')
    ).join(OrderService).join(ServiceOrder).filter(
        and_(
            cast(ServiceOrder.created_at, Date) == date,
            OrderService.status == 'completed'
        )
    ).group_by(Service.id, Service.name).order_by(func.count(OrderService.id).desc()).all()

    # Staff performance (for managers and admins)
    staff_performance = []
    if current_user.role in ['manager', 'admin']:
        staff_performance = db.session.query(
            User.id,
            User.full_name,
            func.count(OrderService.id).label('services_completed'),
            func.sum(OrderService.price_charged).label('revenue_generated')
        ).join(OrderService).filter(
            and_(
                cast(OrderService.completed_at, Date) == date,
                OrderService.status == 'completed'
            )
        ).group_by(User.id, User.full_name).order_by(
            func.count(OrderService.id).desc()
        ).all()

    report = {
        'date': date.isoformat(),
        'summary': {
            'total_orders': len(daily_orders),
            'completed_orders': len(completed_orders),
            'completion_rate': round((len(completed_orders) / len(daily_orders)) * 100, 2) if daily_orders else 0,
            'total_revenue': float(daily_revenue),
            'average_order_value': float(daily_revenue / len(completed_orders)) if completed_orders else 0
        },
        'service_breakdown': [
            {
                'service_name': name,
                'count': count,
                'revenue': float(revenue)
            }
            for name, count, revenue in service_breakdown
        ],
        'staff_performance': [
            {
                'staff_id': staff_id,
                'staff_name': full_name,
                'services_completed': services_completed,
                'revenue_generated': float(revenue_generated)
            }
            for staff_id, full_name, services_completed, revenue_generated in staff_performance
        ],
        'payment_methods': Payment.get_daily_summary(date)['by_method']
    }

    return jsonify({
        'success': True,
        'data': report,
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== USER MANAGEMENT ENDPOINTS ====================

@bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """Get all users (admin only)"""
    include_inactive = request.args.get('include_inactive', 'false').lower() == 'true'

    query = User.query
    if not include_inactive:
        query = query.filter_by(is_active=True)

    users = query.order_by(User.role, User.full_name).all()

    return jsonify({
        'success': True,
        'data': {
            'users': [user.to_dict() for user in users]
        },
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    """Create new user (admin only)"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['username', 'full_name', 'role', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': f'{field.replace("_", " ").title()} is required'
                }
            }), 400

    # Check for existing username
    existing = User.query.filter_by(username=data['username']).first()
    if existing:
        return jsonify({
            'success': False,
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': 'Username already exists'
            }
        }), 400

    # Create user
    user = User(
        username=data['username'],
        full_name=data['full_name'],
        role=data['role'],
        email=data.get('email'),
        phone=data.get('phone')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict()
        },
        'message': 'User created successfully',
        'timestamp': datetime.utcnow().isoformat()
    }), 201

# ==================== STAFF ASSIGNMENT ENDPOINTS ====================

@bp.route('/orders/<int:order_id>/services/<int:service_id>/assign', methods=['POST'])
@login_required
def assign_staff_to_service(order_id, service_id):
    """Assign staff member to a service"""
    data = request.get_json()

    # Find the order service
    order_service = OrderService.query.filter_by(
        order_id=order_id,
        service_id=service_id
    ).first()

    if not order_service:
        return jsonify({
            'success': False,
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Service not found in this order'
            }
        }), 404

    # Validate staff ID
    staff_id = data.get('staff_id')
    if not staff_id:
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Staff ID is required'
            }
        }), 400

    # Check permissions
    if current_user.role == 'staff' and staff_id != current_user.id:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FORBIDDEN',
                'message': 'You can only assign yourself to services'
            }
        }), 403

    success, message = StaffAssignment.assign_staff_to_service(order_service.id, staff_id)

    if success:
        return jsonify({
            'success': True,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': {
                'code': 'ASSIGNMENT_ERROR',
                'message': message
            }
        }), 400

@bp.route('/services/<int:service_id>/complete', methods=['POST'])
@login_required
def complete_service(service_id):
    """Mark service as completed"""
    order_service = OrderService.query.get_or_404(service_id)

    # Check permissions
    if current_user.role == 'staff' and order_service.assigned_staff_id != current_user.id:
        return jsonify({
            'success': False,
            'error': {
                'code': 'FORBIDDEN',
                'message': 'You can only complete services assigned to you'
            }
        }), 403

    if order_service.complete_service():
        return jsonify({
            'success': True,
            'message': 'Service completed successfully',
            'data': {
                'order': order_service.order.to_dict(include_details=True)
            },
            'timestamp': datetime.utcnow().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_STATE',
                'message': 'Service cannot be completed'
            }
        }), 400

# ==================== SEARCH ENDPOINTS ====================

@bp.route('/search', methods=['GET'])
@login_required
def global_search():
    """Global search across all entities"""
    query = request.args.get('q', '').strip()
    entity_type = request.args.get('type', 'all')

    if len(query) < 2:
        return jsonify({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Search query must be at least 2 characters long'
            }
        }), 400

    results = {
        'customers': [],
        'vehicles': [],
        'orders': [],
        'services': []
    }

    # Search customers
    if entity_type in ['all', 'customers']:
        customers = Customer.query.filter(
            or_(
                Customer.phone_number.like(f'%{query}%'),
                Customer.name.like(f'%{query}%'),
                Customer.email.like(f'%{query}%')
            )
        ).limit(10).all()
        results['customers'] = [customer.to_dict() for customer in customers]

    # Search vehicles
    if entity_type in ['all', 'vehicles']:
        vehicles = Vehicle.query.filter(
            or_(
                Vehicle.registration_number.like(f'%{query}%'),
                Vehicle.make.like(f'%{query}%'),
                Vehicle.model.like(f'%{query}%')
            )
        ).limit(10).all()
        results['vehicles'] = [vehicle.to_dict() for vehicle in vehicles]

    # Search orders
    if entity_type in ['all', 'orders']:
        orders = ServiceOrder.query.filter(
            or_(
                ServiceOrder.order_number.like(f'%{query}%'),
                ServiceOrder.notes.like(f'%{query}%')
            )
        ).limit(10).all()
        results['orders'] = [order.to_dict() for order in orders]

    # Search services
    if entity_type in ['all', 'services']:
        services = Service.query.filter(
            or_(
                Service.name.like(f'%{query}%'),
                Service.description.like(f'%{query}%')
            )
        ).limit(10).all()
        results['services'] = [service.to_dict() for service in services]

    return jsonify({
        'success': True,
        'data': {
            'query': query,
            'results': results,
            'total_results': sum(len(results[key]) for key in results)
        },
        'timestamp': datetime.utcnow().isoformat()
    })

# ==================== HEALTH CHECK ====================

@bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'success': True,
        'data': {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
    })