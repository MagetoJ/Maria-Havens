# Maria Havens Hotel & Spa - Local Setup & Deployment Guide

## 🏨 Project Overview

Maria Havens Hotel & Spa is a luxury hotel booking and management system built with Flask, featuring:
- Modern responsive web design
- Room booking and inquiry system
- Admin dashboard for managing bookings and rooms
- SQLite for local development, PostgreSQL for production
- Email notifications for bookings
- Admin user management system

## 🚀 Local Development Setup (Complete ✅)

### Prerequisites
- Python 3.11+ (Currently using Python 3.13.5)
- Virtual environment (already configured)
- All dependencies installed

### Current Status
✅ **Server is running on: http://localhost:5000**
✅ **Database initialized with sample data**
✅ **Admin panel accessible with credentials below**

### Admin Access
- **URL**: http://localhost:5000/admin/login
- **Email**: jabezmageto78@gmail.com
- **Password**: lokeshen@58
- **Role**: Super Admin (can manage other admin users)

### Local Database
- **Type**: SQLite
- **Location**: `c:\Users\DELL\Downloads\Maria Havens\OasisHotelSpa\oasis_hotel.db`
- **Status**: Initialized with 5 rooms, 10 amenities, and 1 admin user

### Key Features Working
- ✅ Homepage with hotel information
- ✅ Rooms & Suites listing with pricing
- ✅ Booking inquiry system
- ✅ Contact forms
- ✅ Admin dashboard
- ✅ Admin login/logout
- ✅ Room management
- ✅ Booking management

## 🌐 Render Deployment Guide

### Step 1: Prerequisites
- GitHub repository with this code
- Render account (https://render.com)

### Step 2: Repository Structure
Ensure these files are in your repository:
- `requirements.txt` ✅
- `render.yaml` ✅
- `Procfile` ✅
- `.env.example` ✅
- `init_db.py` ✅

### Step 3: Deploy via Blueprint (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the branch containing `render.yaml`
   - Click "Create Services"

The `render.yaml` will automatically:
- Create PostgreSQL database (maria-havens-db)
- Create web service (maria-havens)
- Install dependencies
- Initialize database with sample data
- Configure environment variables

### Step 4: Manual Deployment (Alternative)

If Blueprint doesn't work:

1. **Create PostgreSQL Database**
   - New → PostgreSQL
   - Name: `maria-havens-db`
   - Plan: Free

2. **Create Web Service**
   - New → Web Service
   - Connect repository
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt && python init_db.py`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 main:app`

3. **Environment Variables**
   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | (Connect to database) |
   | `SESSION_SECRET` | (Generate 32+ char string) |
   | `FLASK_ENV` | `production` |
   | `FLASK_APP` | `main.py` |

### Step 5: After Deployment

1. **Verify deployment**
   - Check logs in Render dashboard
   - Visit your app URL (e.g., https://maria-havens.onrender.com)

2. **Test key features**
   - Homepage loads
   - Room booking works
   - Admin login functions

3. **Admin Access on Production**
   - URL: `https://your-app-name.onrender.com/admin/login`
   - Email: jabezmageto78@gmail.com
   - Password: lokeshen@58

## 📁 Project Structure

```
OasisHotelSpa/
├── app.py              # Main Flask application
├── main.py            # Entry point
├── models.py          # Database models
├── routes.py          # Application routes
├── forms.py           # WTForms classes
├── config.py          # Configuration
├── init_db.py         # Database initialization
├── requirements.txt   # Python dependencies
├── render.yaml        # Render deployment config
├── Procfile          # Process definition
├── .env              # Local environment variables
├── .env.example      # Environment variables template
├── static/           # CSS, JS, images
├── templates/        # Jinja2 templates
├── attached_assets/  # Generated images
└── oasis_hotel.db   # SQLite database (local)
```

## 🔧 Development Commands

### Start Development Server
```bash
cd "c:\Users\DELL\Downloads\Maria Havens\OasisHotelSpa"
python main.py
```

### Initialize/Reset Database
```bash
python init_db.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 🗃️ Database Schema

### Tables
- **users**: Admin user accounts
- **rooms**: Hotel room types and pricing
- **amenities**: Hotel facilities and services
- **booking_inquiry**: Customer booking requests
- **contact_inquiry**: Customer contact messages

### Sample Data Included
- 5 room types (Deluxe Ocean View, Family Suite, Presidential Suite, Garden View, Spa Wellness Suite)
- 10 amenities (Spa, Pool, Restaurant, Fitness Center, etc.)
- 1 super admin user

## 🎯 Admin Features

- **Dashboard**: Overview of bookings and statistics
- **Room Management**: Add, edit, view room types
- **Booking Management**: View and manage customer inquiries
- **User Management**: Create additional admin users (super admin only)
- **Contact Inquiries**: View customer contact messages

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection with Flask-WTF
- Admin role-based access control
- Secure environment variable handling

## 📧 Email Configuration (Optional)

For production, configure email settings in environment variables:
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@mariahavens.com
```

## 🚨 Troubleshooting

### Local Development Issues

1. **Server won't start**
   - Check if port 5000 is in use: `netstat -an | Select-String ":5000"`
   - Kill existing Python processes if needed

2. **Database errors**
   - Delete `oasis_hotel.db` and run `python init_db.py`

3. **Import errors**
   - Ensure you're in the correct directory
   - Check virtual environment is activated

### Render Deployment Issues

1. **Build failures**
   - Check build logs in Render dashboard
   - Ensure `requirements.txt` is correctly formatted

2. **Database connection errors**
   - Verify DATABASE_URL is correctly set
   - Check database service is running

3. **Application crashes**
   - Check application logs
   - Verify all environment variables are set

## 📞 Support

For issues or questions:
- Review the deployment logs
- Check environment variables
- Ensure database is properly connected
- Contact: jabezmageto78@gmail.com

---

## ✅ Current Status Summary

**Local Development**: ✅ COMPLETE
- Server running on http://localhost:5000
- Database initialized with sample data
- Admin panel accessible and functional
- All core features working

**Ready for Render Deployment**: ✅ YES
- All configuration files prepared
- Database initialization script ready
- Environment variables configured
- Deployment guides provided

Your Maria Havens Hotel & Spa application is fully set up and ready for local development and production deployment! 🎉