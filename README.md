# Maria Havens Hotel & Spa

A modern hotel booking and management system built with Flask and PostgreSQL.

## Features

- Hotel room booking system
- Spa service reservations
- Admin dashboard
- Contact form functionality
- Gallery and amenities showcase
- Responsive design

## Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database (recommended: Render PostgreSQL)
- Git

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MagetoJ/Maria-Havens.git
   cd Maria-Havens
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r pyproject.toml
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your actual database credentials and configuration.

5. Initialize the database:
   ```bash
   python init_db.py
   ```

6. Run the application:
   ```bash
   python main.py
   ```

### Environment Variables

The application requires the following environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for Flask sessions
- `FLASK_ENV`: Environment (development/production)
- `MAIL_SERVER`: SMTP server for email functionality
- `MAIL_USERNAME`: Email username
- `MAIL_PASSWORD`: Email password

### Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the provided `render.yaml` configuration
4. Create a PostgreSQL database on Render
5. The database URL will be automatically configured

### Database Configuration for Render

When setting up PostgreSQL on Render, use these configuration details:

- **Database Name**: `maria_havens_db`
- **Plan**: Free (or upgrade as needed)
- **Region**: Choose closest to your target audience

The connection string format will be:
```
postgresql://username:password@hostname:port/database_name
```

### Project Structure

```
├── app.py              # Flask application factory
├── config.py           # Configuration settings
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── forms.py            # WTForms form definitions
├── init_db.py          # Database initialization script
├── static/             # Static assets (CSS, JS, images)
├── templates/          # Jinja2 templates
├── render.yaml         # Render deployment configuration
└── Procfile           # Process file for deployment
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### License

This project is licensed under the MIT License.