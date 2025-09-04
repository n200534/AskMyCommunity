# AskMyCommunity Backend API

A FastAPI-based backend for the AskMyCommunity application that helps users discover amazing places in their city.

## Features

- **Places Management**: CRUD operations for places with search and filtering
- **User Authentication**: User registration, login, and profile management
- **AI Recommendations**: Intelligent place recommendations based on user queries
- **Search Analytics**: Track search queries and user behavior
- **Location-based Search**: Find places near user location
- **Reviews and Ratings**: User reviews and place ratings system

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL/SQLite**: Database (configurable)
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Alembic**: Database migrations

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=sqlite:///./askmycommunity.db
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### 3. Run the Application

```bash
# Development mode
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Seed Sample Data (Optional)

```bash
python -m app.utils.seed_data
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Places
- `GET /api/v1/places/` - Get all places with filtering
- `GET /api/v1/places/{place_id}` - Get specific place
- `POST /api/v1/places/search` - Search places with advanced filters
- `POST /api/v1/places/` - Create new place
- `PUT /api/v1/places/{place_id}` - Update place
- `DELETE /api/v1/places/{place_id}` - Delete place
- `POST /api/v1/places/{place_id}/like` - Like/unlike place

### Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Recommendations
- `GET /api/v1/recommendations/` - Get user recommendations
- `POST /api/v1/recommendations/` - Create recommendation
- `PUT /api/v1/recommendations/{id}` - Update recommendation
- `GET /api/v1/recommendations/ai-suggestions` - Get AI suggestions
- `POST /api/v1/recommendations/search` - Log search query

## Database Models

### Place
- Basic place information (name, description, type, address)
- Location data (latitude, longitude)
- Rating and price information
- Amenities and opening hours
- Verification status

### User
- User profile information
- Authentication data
- Preferences and settings

### Recommendation
- AI-generated recommendations
- User feedback and interaction tracking
- Search query logging

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── places.py
│   │           ├── users.py
│   │           └── recommendations.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── place.py
│   │   ├── user.py
│   │   └── recommendation.py
│   ├── schemas/
│   │   ├── place.py
│   │   ├── user.py
│   │   └── recommendation.py
│   ├── services/
│   │   └── ai_service.py
│   ├── utils/
│   │   └── seed_data.py
│   └── main.py
├── requirements.txt
├── .env.example
└── README.md
```

### Adding New Features

1. **Models**: Add new database models in `app/models/`
2. **Schemas**: Create Pydantic schemas in `app/schemas/`
3. **Endpoints**: Add API endpoints in `app/api/v1/endpoints/`
4. **Services**: Add business logic in `app/services/`

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Deployment

### Docker

```bash
# Build image
docker build -t askmycommunity-api .

# Run container
docker run -p 8000:8000 askmycommunity-api
```

### Environment Variables

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Debug mode (True/False)
- `CORS_ORIGINS`: Allowed CORS origins

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
