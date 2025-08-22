# AskMyCommunity – AI-Powered Local Recommender

An intelligent local recommendation system that uses AI to suggest places to hang out, restaurants, activities, and events based on scraped data from Google Maps, Reddit, and local blogs.

## Features

- **AI-Powered Recommendations**: Uses Google Gemini Flash API to generate personalized local suggestions
- **Multi-Source Data**: Scrapes Google Maps, Reddit, and local blogs for comprehensive local information
- **Smart Query Processing**: Natural language queries like "Where should I hang out on Saturday?"
- **Social Voting**: Community-driven rating and voting system
- **Event Planner Mode**: Plan and discover local events
- **Modern UI**: Beautiful Next.js frontend with responsive design

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Google Gemini Flash API**: AI-powered recommendation engine
- **Playwright**: Web scraping and automation
- **MongoDB**: NoSQL database for flexible data storage
- **Pydantic**: Data validation and serialization

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/ui**: Beautiful, accessible UI components
- **React Hook Form**: Form handling and validation

## Project Structure

```
ASKMYCOMMUNITY/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration and utilities
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── scrapers/       # Web scraping modules
│   ├── requirements.txt
│   └── main.py
├── frontend/                # Next.js frontend
│   ├── app/                # App Router pages
│   ├── components/         # Reusable UI components
│   ├── lib/                # Utilities and configurations
│   ├── types/              # TypeScript type definitions
│   └── package.json
└── README.md
```

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend URL
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

### Frontend (.env.local)
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

## API Endpoints

- `POST /api/recommendations/query` - Get AI-powered recommendations
- `GET /api/places/{place_id}` - Get place details
- `POST /api/places/{place_id}/vote` - Vote on a place
- `GET /api/events` - Get local events
- `POST /api/events` - Create new event

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
