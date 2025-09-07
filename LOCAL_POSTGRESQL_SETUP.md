# Local PostgreSQL Setup for Maria Havens

## Install PostgreSQL Locally

### Option 1: PostgreSQL Official Installer (Recommended)
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. **Important**: Remember your PostgreSQL superuser password!
4. Default port is 5432 (keep this)

### Option 2: Using Docker (Alternative)
```bash
docker run --name maria-havens-postgres -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=maria_havens_local -p 5432:5432 -d postgres:15
```

## Database Setup

### 1. Create Local Database
Open PostgreSQL command line (psql) or use pgAdmin:

```sql
-- Connect as postgres superuser
CREATE DATABASE maria_havens_local;
CREATE USER maria_havens_user WITH PASSWORD 'lokeshen@58';
GRANT ALL PRIVILEGES ON DATABASE maria_havens_local TO maria_havens_user;
```

### 2. Configure Environment Variables
Create a `.env` file in your project root:

```env
# Local PostgreSQL Configuration
DATABASE_URL=postgresql://maria_havens_user:lokeshen@58@localhost:5432/maria_havens_local

# Session Secret Key
SESSION_SECRET=your-super-secret-session-key-change-this-in-production

# Flask Environment
FLASK_ENV=development
FLASK_APP=main.py

# Email configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=jabezmageto78@gmail.com
MAIL_PASSWORD=kwjn rrno dnbm usxl
MAIL_DEFAULT_SENDER=jabezmageto78@gmail.com
```

## Example Local Database URLs

Choose one of these formats for your `.env` file:

### Standard Format (Recommended)
```
DATABASE_URL=postgresql://maria_havens_user:lokeshen@58@localhost:5432/maria_havens_local
```

### If using default postgres user
```
DATABASE_URL=postgresql://postgres:lokeshen@58@localhost:5432/maria_havens_local
```

### With specific host (if needed)
```
DATABASE_URL=postgresql://username:password@127.0.0.1:5432/maria_havens_local
```

## Test Your Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database**:
   ```bash
   python init_db.py
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Verify it works**:
   - Go to http://localhost:5000
   - Check admin login at http://localhost:5000/admin/login
   - Credentials: jabezmageto78@gmail.com / lokeshen@58

## Common Issues & Solutions

### Connection Error: "could not connect to server"
- Ensure PostgreSQL service is running
- Check if port 5432 is available
- Verify username/password in DATABASE_URL

### Permission Denied
- Make sure user has proper privileges on the database
- Try using postgres superuser initially for testing

### Database Does Not Exist
- Create the database first: `CREATE DATABASE maria_havens_local;`
- Ensure database name matches your DATABASE_URL

## Production vs Local

### Local Development
- Uses `postgresql://user:pass@localhost:5432/maria_havens_local`
- FLASK_ENV=development
- Debug mode enabled

### Production (Render)
- Uses Render's managed PostgreSQL database
- FLASK_ENV=production
- Debug mode disabled
- Automatic SSL/TLS encryption

Your project is already configured to work with both environments seamlessly!