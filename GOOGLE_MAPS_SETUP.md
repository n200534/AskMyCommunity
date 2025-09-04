# Google Maps & Gemini Flash Integration Setup

## Overview

Your AskMyCommunity app now integrates with:
- **Google Maps API** for real places data and directions
- **Gemini Flash AI** for intelligent recommendations
- **Interactive maps** with place markers and directions

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./askmycommunity.db

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

### 3. Get API Keys

#### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Places API
   - Directions API
   - Maps JavaScript API
4. Create credentials (API Key)
5. Restrict the key to your domains

#### Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Go to API Keys section
4. Create new API key
5. Copy the key to your `.env` file

### 4. Run Backend

```bash
cd backend
python run.py
```

The API will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create a `.env.local` file in the frontend directory:

```env
# Google Maps API Key
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Frontend

```bash
cd frontend
npm run dev
```

The app will be available at `http://localhost:3000`

## Features

### 🗺️ **Interactive Maps**
- Real-time Google Maps integration
- Place markers with custom icons
- Click to select places
- Responsive map that fits all markers

### 🤖 **AI-Powered Recommendations**
- Gemini Flash AI for intelligent suggestions
- Context-aware recommendations
- Confidence scoring
- Natural language understanding

### 🧭 **Directions & Navigation**
- Step-by-step directions
- Multiple travel modes (driving, walking, transit)
- Distance and duration estimates
- Open in Google Maps integration

### 🔍 **Advanced Search**
- Real places from Google Maps
- Filter by type, rating, price
- Location-based search
- AI-enhanced results

### 📱 **Responsive Design**
- Mobile-friendly interface
- Toggle map view
- Optimized for all screen sizes

## API Endpoints

### Maps & Places
- `POST /api/v1/maps/search` - Search places with AI
- `GET /api/v1/maps/nearby` - Get nearby places
- `GET /api/v1/maps/place/{id}` - Get place details
- `GET /api/v1/maps/directions` - Get directions

### AI Recommendations
- `GET /api/v1/recommendations/ai-suggestions` - AI suggestions
- `POST /api/v1/recommendations/search` - Log search queries

## Usage Examples

### Search for Places
```typescript
const searchRequest = {
  query: "romantic dinner spots",
  place_type: "restaurant",
  min_rating: 4.0,
  latitude: 12.9716,
  longitude: 77.5946,
  radius: 5,
  page: 1,
  page_size: 20,
  sort_by: "relevance"
};

const response = await searchPlaces(searchRequest);
```

### Get Directions
```typescript
const directions = await getDirections(
  userLat, userLng,  // Origin
  placeLat, placeLng, // Destination
  'driving' // Mode
);
```

### AI Recommendations
```typescript
const recommendations = await ai_factory.generate_recommendations(
  "cozy cafe for work",
  availablePlaces,
  userPreferences,
  5
);
```

## Cost Estimation

### Google Maps API
- **Places API**: $0.017 per request
- **Directions API**: $0.005 per request
- **Maps JavaScript API**: $0.007 per 1,000 loads

### Google AI (Gemini Flash)
- **Input**: $0.000075 per 1K tokens
- **Output**: $0.0003 per 1K tokens
- **Estimated cost per recommendation**: ~$0.001-0.005

## Troubleshooting

### Common Issues

1. **Maps not loading**
   - Check API key is correct
   - Ensure Maps JavaScript API is enabled
   - Check domain restrictions

2. **Places not found**
   - Verify Places API is enabled
   - Check API key permissions
   - Ensure billing is set up

3. **AI recommendations not working**
   - Check Google AI API key
   - Verify AI service configuration
   - Check API quotas

4. **CORS errors**
   - Add frontend URL to CORS_ORIGINS
   - Check backend CORS configuration

### Debug Mode

Enable debug mode in backend `.env`:
```env
DEBUG=True
```

This will show detailed error logs and API responses.

## Production Deployment

### Environment Variables
Set these in your production environment:

**Backend:**
- `GOOGLE_MAPS_API_KEY`
- `GOOGLE_AI_API_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`

**Frontend:**
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`
- `NEXT_PUBLIC_API_URL`

### Security
- Restrict API keys to specific domains
- Use environment variables for all secrets
- Enable API quotas and monitoring
- Implement rate limiting

## Next Steps

1. **Set up API keys** following the instructions above
2. **Test the integration** with sample searches
3. **Customize the UI** to match your brand
4. **Add more features** like favorites, reviews, etc.
5. **Deploy to production** when ready

Your AskMyCommunity app is now powered by Google Maps and Gemini Flash AI! 🚀
