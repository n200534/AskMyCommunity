# Neon Database Migration Guide

## 🚀 Quick Setup Steps

### 1. Create Neon Database

1. **Go to [Neon Console](https://console.neon.tech/)**
2. **Sign up/Login** with GitHub (recommended)
3. **Create New Project**:
   - Project name: `askmycommunity`
   - Region: Choose closest to your location
   - PostgreSQL version: Latest (15+)
4. **Copy Connection String** from the dashboard

### 2. Update Environment Variables

Create/update your `.env` file in the backend directory:

```env
# Neon Database Connection
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require

# Optional: Other settings
SECRET_KEY=your-secret-key-change-in-production-12345
DEBUG=True
```

### 3. Install Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Database Migration

```bash
# Set the DATABASE_URL environment variable
export DATABASE_URL="your-neon-connection-string-here"

# Create the initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to create tables
alembic upgrade head
```

### 5. Test the Setup

```bash
# Test database connection
python -c "
from database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('✅ Database connection successful!')
"

# Start the server
python server.py
```

## 📁 Files Created

### Backend Structure
```
backend/
├── server.py              # Main server with Neon integration
├── database.py            # Database models and configuration
├── requirements.txt       # Updated with PostgreSQL dependencies
├── alembic/              # Database migration files
│   ├── env.py            # Alembic configuration
│   └── versions/         # Migration files
├── alembic.ini           # Alembic settings
└── .env                  # Environment variables
```

### Database Models
- **Place**: Stores place information (name, address, coordinates, rating, etc.)
- **User**: User accounts and authentication
- **Recommendation**: AI recommendations and user interactions

## 🔧 Migration Commands

### Create New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

### Check Migration Status
```bash
alembic current
alembic history
```

## 🧪 Testing the API

### 1. Start the Server
```bash
python server.py
```

### 2. Test Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Search Places:**
```bash
curl -X POST http://localhost:8000/api/v1/maps/search \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee", "page": 1, "page_size": 10}'
```

**Get All Places:**
```bash
curl http://localhost:8000/api/v1/places
```

**API Documentation:**
Visit http://localhost:8000/docs for interactive API documentation.

## 🚨 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Verify your Neon connection string
   - Check if your IP is whitelisted
   - Ensure SSL mode is set to `require`

2. **Migration Errors**
   - Make sure DATABASE_URL is set correctly
   - Check if the database exists
   - Verify your credentials

3. **Import Errors**
   - Ensure all dependencies are installed
   - Check Python path and virtual environment

### Connection String Format
```env
# Correct format
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require

# With additional parameters
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require&connect_timeout=10
```

## 🎯 Next Steps

1. **Set up your Neon database** following the steps above
2. **Update your .env file** with the real connection string
3. **Run the migration** to create tables
4. **Start the server** and test the API
5. **Connect the frontend** to the new backend

## 📊 Database Features

### Neon-Specific Benefits
- **Serverless**: No server management required
- **Auto-scaling**: Handles traffic spikes automatically
- **Branching**: Create database branches for development
- **Free Tier**: 3GB storage, 10GB transfer per month
- **Global**: Fast worldwide access

### Tables Created
- `places` - Store place information
- `users` - User accounts and profiles
- `recommendations` - AI recommendations and interactions

Your AskMyCommunity app is now ready with a powerful Neon PostgreSQL database! 🎉
