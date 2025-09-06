# The Oasis Hotel & Spa

## Overview

The Oasis Hotel & Spa is a luxury hotel booking and management web application built with Flask. The application serves as both a comprehensive online brochure and a functional booking engine, allowing guests to explore rooms, amenities, and services while submitting booking inquiries. The system features a modern, responsive design with multiple pages showcasing the hotel's offerings, an inquiry-based booking system, and contact management functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension for database operations
- **Form Handling**: Flask-WTF with WTForms for secure form processing and validation
- **Email System**: Flask-Mail for sending booking confirmations and contact inquiries
- **Session Management**: Flask's built-in session handling with configurable secret keys

### Frontend Architecture
- **Template Engine**: Jinja2 templates with template inheritance using a base template
- **CSS Framework**: Bootstrap 5 for responsive design and UI components
- **Icons**: Font Awesome for iconography
- **JavaScript**: Vanilla JavaScript for interactive features and form enhancements
- **Responsive Design**: Mobile-first approach with Bootstrap's grid system

### Database Design
- **Room Management**: Rooms table storing room details, pricing, occupancy, and amenities
- **Amenities System**: Separate amenities table with categorization for spa, dining, fitness, etc.
- **Booking System**: Inquiry-based booking system storing guest information and preferences
- **Contact Management**: Contact inquiries table for general customer communication
- **Data Relationships**: Foreign key relationships between bookings and rooms

### Application Structure
- **Route Organization**: Separated routes module for clean code organization
- **Model Definitions**: Dedicated models module for database schema
- **Form Classes**: Centralized form definitions with validation logic
- **Configuration Management**: Environment-based configuration with development and production settings
- **Database Initialization**: Automated table creation and sample data seeding

### Email Integration
- **SMTP Configuration**: Configurable email settings for different providers
- **Notification System**: Automated email notifications for booking inquiries and contact forms
- **Template-based Emails**: Structured email templates for consistent communication

## External Dependencies

### Core Dependencies
- **Flask**: Web framework for routing, templating, and request handling
- **SQLAlchemy**: Database toolkit and ORM for data persistence
- **PostgreSQL**: Primary database system for production deployment
- **Flask-Mail**: Email sending capability for notifications and confirmations

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN for responsive design
- **Font Awesome 6**: Icon library loaded via CDN for UI icons
- **jQuery**: JavaScript library for enhanced interactivity (implied by Bootstrap usage)

### Development Tools
- **WTForms**: Form validation and rendering library
- **Werkzeug**: WSGI toolkit with proxy fix middleware for deployment
- **Python-dotenv**: Environment variable management (implied by os.environ usage)

### Production Considerations
- **Database Connection**: PostgreSQL with connection pooling and health checks
- **Email Services**: SMTP configuration for Gmail or other email providers
- **Environment Variables**: Secure configuration management for sensitive data
- **Session Security**: Configurable session secret keys for production deployment