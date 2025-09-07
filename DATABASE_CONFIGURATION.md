# Maria Havens - Database Configuration Guide

## 🔗 Database URLs for All Environments

### Local Development (PostgreSQL)
```env
# Standard local setup with custom user
DATABASE_URL=postgresql://maria_havens_user:lokeshen@58@localhost:5432/maria_havens_local

# Alternative: Using default postgres user
DATABASE_URL=postgresql://postgres:lokeshen@58@localhost:5432/maria_havens_local

# Docker setup
DATABASE_URL=postgresql://postgres:lokeshen@58@localhost:5432/maria_havens_local
```

### Production on Render
Render will automatically provide these URLs when you create the PostgreSQL service:

#### External Database URL (for external connections)
```
DATABASE_URL=postgresql://[username]:[password]@[hostname]:5432/[database_name]
```
Example format:
```
DATABASE_URL=postgresql://maria_havens_db_user:abc123xyz@dpg-xxxxxxxx-a.oregon-postgres.render.com:5432/maria_havens_db
```

#### Internal Database URL (for connections within Render - recommended)
```
DATABASE_URL_INTERNAL=postgresql://[username]:[password]@[hostname]/[database_name]
```
Example format:
```
DATABASE_URL_INTERNAL=postgresql://maria_havens_db_user:abc123xyz@dpg-xxxxxxxx-a/maria_havens_db
```

### Key Differences:
- **External URL**: Includes port `:5432` - used for connections from outside Render
- **Internal URL**: No port - used for faster connections between Render services
- **Your app will use the DATABASE_URL automatically** - Render sets this up for you

## 📧 Email Configuration (Updated)

All environments now use:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=jabezmageto78@gmail.com
MAIL_PASSWORD=kwjn rrno dnbm usxl
MAIL_DEFAULT_SENDER=jabezmageto78@gmail.com
```

## 🚀 Quick Setup Commands

### For Local Development:
1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE maria_havens_local;
   CREATE USER maria_havens_user WITH PASSWORD 'lokeshen@58';
   GRANT ALL PRIVILEGES ON DATABASE maria_havens_local TO maria_havens_user;
   ```

2. **Create `.env` file:**
   ```env
   DATABASE_URL=postgresql://maria_havens_user:lokeshen@58@localhost:5432/maria_havens_local
   SESSION_SECRET=your-dev-secret-key
   FLASK_ENV=development
   FLASK_APP=main.py
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=jabezmageto78@gmail.com
   MAIL_PASSWORD=kwjn rrno dnbm usxl
   MAIL_DEFAULT_SENDER=jabezmageto78@gmail.com
   ```

3. **Initialize and run:**
   ```bash
   pip install -r requirements.txt
   python init_db.py
   python main.py
   ```

### For Docker Development:
```bash
# Start PostgreSQL container
docker run --name maria-havens-postgres \
  -e POSTGRES_PASSWORD=lokeshen@58 \
  -e POSTGRES_DB=maria_havens_local \
  -p 5432:5432 -d postgres:15

# Use this DATABASE_URL
DATABASE_URL=postgresql://postgres:lokeshen@58@localhost:5432/maria_havens_local
```

## ✅ Render Deployment Ready

Your project is configured to automatically:
- **Connect to Render PostgreSQL** via the DATABASE_URL environment variable
- **Initialize database** with sample data during deployment
- **Send emails** using the configured Gmail credentials
- **Handle both internal and external database connections**

The `render.yaml` file is fully configured with all necessary environment variables including the email settings!