# The Spot - Car Wash Management System

## Overview
A comprehensive, mobile-first car wash management system designed for The Spot in Kenya. The system transforms paper-based operations into a professional digital platform with real-time queue management, payment processing, and business analytics.

## Project Architecture

### Backend (Python/Flask)
- **Framework**: Flask 2.3+ with extensions
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **ORM**: SQLAlchemy with Flask-Migrate for migrations
- **Authentication**: Flask-Login with session management
- **Location**: `/backend/`

### Frontend (Bootstrap 5 + Jinja2)
- **UI Framework**: Bootstrap 5.3 with custom CSS
- **Templates**: Jinja2 templates extending base.html
- **JavaScript**: Vanilla JS for interactivity
- **Location**: `/frontend/`

### Key Files
- `backend/run.py` - Application entry point
- `backend/config.py` - Configuration settings
- `backend/app/__init__.py` - Flask app factory
- `backend/app/routes/` - Route blueprints (main, auth, api)
- `backend/app/models/` - Database models
- `frontend/templates/` - Jinja2 templates
- `frontend/static/` - CSS and JavaScript files

## Database Models
1. **User** - Staff accounts with roles (admin, manager, staff)
2. **Customer** - Customer profiles with phone number lookup
3. **Vehicle** - Vehicle registration and service history
4. **Service** - Car wash services with pricing
5. **ServiceOrder** - Order tracking with status workflow
6. **OrderService** - Services linked to orders with staff assignment
7. **Payment** - Payment records with multiple methods
8. **StaffAssignment** - Staff assignment tracking

## Demo Accounts
| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| Staff | staff | staff123 |

## Development Setup
The app runs on port 5000 using the Flask development server with SQLite database.

```bash
cd backend
USE_SQLITE=true python run.py
```

## Production Deployment
Uses Gunicorn WSGI server for production:

```bash
cd backend
gunicorn --bind 0.0.0.0:5000 --workers 4 --reuse-port run:app
```

## Recent Changes
- Initial project import from GitHub
- Created missing templates (customers, vehicles, services, reports, staff, settings, profile, errors)
- Fixed missing imports (or_) in main.py
- Added `now` variable to payments route
- Configured workflow for Replit environment

## User Preferences
- Mobile-first design with Bootstrap 5
- Kenyan Shilling (KES) currency format
- M-Pesa, Airtel Money, Cash, and Card payment methods
- Touch-optimized interface for car wash staff

## Features
- Dashboard with real-time statistics
- Service queue management with status tracking
- Customer and vehicle database
- Payment recording with receipts
- Staff workload tracking
- Daily reports and analytics
