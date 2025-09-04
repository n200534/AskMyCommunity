# Environment Setup Guide

## Backend Environment File

Create a `.env` file in the `backend/` directory with the following content:

```env
# Database Configuration (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require
# Get your connection string from: https://console.neon.tech/

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

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

## Frontend Environment File

Create a `.env.local` file in the `frontend/` directory with the following content:

```env
# Google Maps API Key
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# App Configuration
NEXT_PUBLIC_APP_NAME=AskMyCommunity
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## How to Get API Keys

### 1. Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Places API
   - Directions API
   - Maps JavaScript API
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key and replace `your-google-maps-api-key-here`

### 2. Google AI API Key (Gemini Flash)

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Go to "Get API Key" section
4. Create new API key
5. Copy the API key and replace `your-google-ai-api-key-here`

### 3. Neon Database Setup

1. Go to [Neon Console](https://console.neon.tech/)
2. Sign up/Login with GitHub
3. Create a new project
4. Copy the connection string from the dashboard
5. Replace `your-neon-connection-string-here` in .env

## Database Configuration (Neon PostgreSQL)

### Neon Database Setup
1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project
3. Copy the connection string from the dashboard
4. Replace the DATABASE_URL in your .env file

### Connection String Format
```env
DATABASE_URL=postgresql://username:password@ep-xxxxx.us-east-1.aws.neon.tech/askmycommunity?sslmode=require
```

### Alternative: Local PostgreSQL
```env
DATABASE_URL=postgresql://username:password@localhost:5432/askmycommunity
```

## Security Notes

1. **Never commit .env files to version control**
2. **Change the SECRET_KEY in production**
3. **Restrict API keys to specific domains**
4. **Use strong passwords for database**

## File Structure

```
ASKMYCOMMUNITY/
├── backend/
│   ├── .env                 # Backend environment variables
│   └── env_template.txt     # Template for reference
├── frontend/
│   ├── .env.local          # Frontend environment variables
│   └── env_template.txt    # Template for reference
└── ENVIRONMENT_SETUP.md    # This guide
```

## Quick Setup Commands

```bash
# Backend
cd backend
cp env_template.txt .env
# Edit .env with your actual API keys

# Frontend
cd frontend
cp env_template.txt .env.local
# Edit .env.local with your actual API keys
```

## Verification

After setting up the environment files:

1. **Backend**: Run `python run.py` - should start without errors
2. **Frontend**: Run `npm run dev` - should load without API key errors
3. **Test**: Try searching for places to verify Google Maps integration

## Troubleshooting

### Common Issues

1. **"API key not found"** - Check if .env files exist and have correct variable names
2. **"CORS error"** - Ensure frontend URL is in CORS_ORIGINS
3. **"Database connection failed"** - Check DATABASE_URL format
4. **"Maps not loading"** - Verify Google Maps API key and enabled APIs

### Debug Mode

Set `DEBUG=True` in backend .env to see detailed error logs.

## Production Deployment

For production, set these environment variables in your hosting platform:

**Backend:**
- `DATABASE_URL`
- `GOOGLE_MAPS_API_KEY`
- `GOOGLE_AI_API_KEY`
- `SECRET_KEY`
- `CORS_ORIGINS`

**Frontend:**
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
- `NEXT_PUBLIC_API_URL`
