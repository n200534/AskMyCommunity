# Neon Database Setup Guide

## What is Neon?

Neon is a serverless PostgreSQL database that's perfect for modern applications. It offers:
- **Serverless architecture** - No server management
- **Automatic scaling** - Handles traffic spikes
- **Branching** - Database branches for development
- **Free tier** - Generous free usage
- **Global availability** - Fast worldwide access

## Setup Steps

### 1. Create Neon Account

1. Go to [Neon Console](https://console.neon.tech/)
2. Sign up with GitHub (recommended)
3. Verify your email

### 2. Create New Project

1. Click "Create Project"
2. Choose a project name: `askmycommunity`
3. Select a region close to your users
4. Choose PostgreSQL version (latest recommended)
5. Click "Create Project"

### 3. Get Connection String

1. In your project dashboard, go to "Connection Details"
2. Copy the connection string (it looks like this):
   ```
   postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require
   ```
3. Replace the `DATABASE_URL` in your `.env` file

### 4. Test Connection

```bash
cd backend
python -c "
from app.core.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('Database connection successful!')
"
```

## Environment Configuration

### Backend (.env)
```env
# Neon Database
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require

# Security
SECRET_KEY=your-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Google AI (Gemini Flash)
GOOGLE_AI_API_KEY=your-google-ai-api-key-here

# AI Service Configuration
AI_SERVICE=google_ai

# App Settings
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Database Migration

### 1. Install Alembic (if not already installed)
```bash
pip install alembic
```

### 2. Initialize Alembic
```bash
cd backend
alembic init alembic
```

### 3. Create Migration
```bash
alembic revision --autogenerate -m "Initial migration"
```

### 4. Apply Migration
```bash
alembic upgrade head
```

## Neon-Specific Features

### 1. Database Branching
- Create branches for different environments
- Test changes without affecting production
- Merge branches when ready

### 2. Connection Pooling
- Neon handles connection pooling automatically
- No need to configure connection limits
- Optimized for serverless applications

### 3. Monitoring
- Built-in query performance monitoring
- Connection metrics
- Usage analytics

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check if your IP is whitelisted
   - Verify connection string format
   - Ensure SSL mode is set to `require`

2. **Authentication Failed**
   - Verify username and password
   - Check if database exists
   - Ensure connection string is complete

3. **SSL Certificate Error**
   - Add `?sslmode=require` to connection string
   - Or use `?sslmode=disable` for development (not recommended for production)

### Connection String Format

```env
# Correct format
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require

# With additional parameters
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require&connect_timeout=10
```

## Production Considerations

### 1. Environment Variables
Set these in your production environment:
- `DATABASE_URL` - Your Neon connection string
- `SECRET_KEY` - Strong secret key
- `GOOGLE_MAPS_API_KEY` - Google Maps API key
- `GOOGLE_AI_API_KEY` - Google AI API key

### 2. Security
- Use strong passwords
- Enable SSL (sslmode=require)
- Restrict database access by IP if needed
- Regular security updates

### 3. Monitoring
- Set up database monitoring
- Monitor query performance
- Track connection usage
- Set up alerts for issues

## Free Tier Limits

Neon's free tier includes:
- **3GB storage**
- **10GB transfer per month**
- **Unlimited connections**
- **7-day backup retention**

This is more than enough for development and small production apps.

## Next Steps

1. **Set up your Neon database** following the steps above
2. **Update your .env file** with the connection string
3. **Test the connection** using the test script
4. **Run migrations** to create tables
5. **Start your application** and verify everything works

Your AskMyCommunity app is now ready to use Neon's powerful PostgreSQL database! 🚀
