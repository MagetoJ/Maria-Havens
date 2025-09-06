# Maria Havens Hotel & Spa - Render Deployment Guide

This guide provides step-by-step instructions for deploying the Maria Havens Hotel & Spa application to Render with PostgreSQL database.

## Prerequisites

- GitHub account with the Maria Havens repository
- Render account (https://render.com)

## Step 1: Set Up PostgreSQL Database on Render

1. **Log in to Render Dashboard**
   - Go to https://dashboard.render.com
   - Sign in with your account

2. **Create PostgreSQL Database**
   - Click "New +" button
   - Select "PostgreSQL"
   - Configure the database:
     - **Name**: `maria-havens-db`
     - **Database**: `maria_havens_db`
     - **User**: `maria_havens_user` (or leave default)
     - **Region**: Choose closest to your target audience
     - **PostgreSQL Version**: 15+ (recommended)
     - **Plan**: Free (for development) or paid plan

3. **Note Database Connection Details**
   After creation, save these connection details:
   - **External Database URL**: `postgresql://username:password@hostname:port/database`
   - **Internal Database URL**: `postgresql://username:password@hostname/database`
   - **Hostname**: `dpg-xxxxx-a.region-postgres.render.com`
   - **Port**: `5432`
   - **Database**: `maria_havens_db`
   - **Username**: Your database username
   - **Password**: Generated password

## Step 2: Configure Environment Variables

1. **Update Local .env File** (for local development):
   ```env
   # Replace with your actual Render PostgreSQL connection string
   DATABASE_URL=postgresql://[username]:[password]@[hostname]:5432/maria_havens_db
   
   # Generate a strong secret key for production
   SESSION_SECRET=your-super-secure-session-key-min-32-characters
   
   # Flask Environment
   FLASK_ENV=production
   FLASK_APP=main.py
   
   # Optional: Email configuration
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@mariahavens.com
   ```

## Step 3: Deploy Web Service on Render

1. **Create New Web Service**
   - In Render Dashboard, click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/MagetoJ/Maria-Havens.git`

2. **Configure Web Service**
   - **Name**: `maria-havens`
   - **Root Directory**: Leave empty (or set to `/OasisHotelSpa` if needed)
   - **Environment**: `Python 3`
   - **Region**: Same as database region
   - **Branch**: `main`
   - **Build Command**:
     ```bash
     pip install -r pyproject.toml && python init_db.py
     ```
   - **Start Command**:
     ```bash
     gunicorn --bind 0.0.0.0:$PORT main:app
     ```

3. **Environment Variables**
   Add these environment variables in the Render dashboard:

   | Key | Value |
   |-----|--------|
   | `DATABASE_URL` | Connect to your maria-havens-db (Render will auto-populate) |
   | `SESSION_SECRET` | Generate a secure random string (32+ characters) |
   | `FLASK_ENV` | `production` |
   | `FLASK_APP` | `main.py` |
   | `MAIL_SERVER` | `smtp.gmail.com` (optional) |
   | `MAIL_PORT` | `587` (optional) |
   | `MAIL_USE_TLS` | `true` (optional) |
   | `MAIL_USERNAME` | Your email (optional) |
   | `MAIL_PASSWORD` | Your app password (optional) |
   | `MAIL_DEFAULT_SENDER` | `noreply@mariahavens.com` (optional) |

4. **Auto-Deploy Settings**
   - Enable "Auto-Deploy" to deploy automatically on git push

## Step 4: Alternative - Deploy with render.yaml

The repository includes a `render.yaml` file for automated deployment:

1. **Push render.yaml to your repository** (already included)
2. **In Render Dashboard**:
   - Go to "Blueprint" → "New Blueprint Instance"
   - Connect your repository
   - Select the branch containing `render.yaml`
   - Review and create services

The `render.yaml` will automatically:
- Create the PostgreSQL database
- Set up the web service
- Configure environment variables
- Link database connection

## Step 5: Database Initialization

After deployment:

1. **Check Deployment Logs**
   - Go to your web service in Render dashboard
   - Check "Logs" tab for any errors

2. **Manual Database Initialization** (if needed):
   - If `init_db.py` didn't run during build, you can trigger it manually
   - Go to web service → "Shell" tab (if available on your plan)
   - Run: `python init_db.py`

## Step 6: Verify Deployment

1. **Access Your Application**
   - Your app will be available at: `https://maria-havens.onrender.com` (or similar)
   - Render provides the URL in your service dashboard

2. **Test Key Features**:
   - Homepage loads correctly
   - Room booking system works
   - Contact form functions (if email configured)
   - Admin dashboard accessible

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify DATABASE_URL is correctly set
   - Check database is running and accessible
   - Ensure SSL mode is enabled (`PGSSLMODE=require`)

2. **Build Failures**
   - Check Python version compatibility
   - Verify all dependencies in `pyproject.toml`
   - Review build logs for specific errors

3. **Import Errors**
   - Ensure all Python files are properly structured
   - Check for missing `__init__.py` files if needed

4. **Static Files Not Loading**
   - Verify static file paths in templates
   - Check Flask static folder configuration

### Security Checklist

- [ ] Strong SESSION_SECRET (32+ characters, random)
- [ ] Database credentials secured
- [ ] Environment variables properly set
- [ ] Email credentials protected (if used)
- [ ] Debug mode disabled in production
- [ ] HTTPS enabled (automatic with Render)

### Performance Optimization

- [ ] Database connection pooling configured
- [ ] Static file caching enabled
- [ ] Database indexes optimized
- [ ] Consider upgrading to paid plans for better performance

## Environment Variables Reference

```env
# Core Application
DATABASE_URL=postgresql://user:pass@host:5432/db
SESSION_SECRET=your-secure-session-key
FLASK_ENV=production
FLASK_APP=main.py

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@mariahavens.com

# Database Components (Auto-configured, but useful for reference)
DB_HOST=dpg-xxxxx-a.region-postgres.render.com
DB_PORT=5432
DB_NAME=maria_havens_db
DB_USER=username
DB_PASSWORD=password
PGSSLMODE=require
```

## Support

For deployment issues:
- Check Render documentation: https://render.com/docs
- Review application logs in Render dashboard
- Verify environment variables and database connections

## Next Steps

After successful deployment:
1. Set up custom domain (if desired)
2. Configure monitoring and alerts
3. Set up automated backups for database
4. Implement CI/CD pipeline for automated testing
5. Consider upgrading to paid plans for production use