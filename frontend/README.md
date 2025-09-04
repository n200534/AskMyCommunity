# AskMyCommunity Frontend

A modern Next.js frontend for discovering places with AI-powered recommendations.

## Features

- **Search Interface**: Natural language search for places
- **Google Maps Integration**: Interactive maps with place markers
- **Place Discovery**: Browse and filter places by type, rating, price
- **Directions**: Get step-by-step directions to any place
- **Responsive Design**: Works on desktop and mobile

## Quick Start

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Set Environment Variables**:
   Create `.env.local`:
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Run Development Server**:
   ```bash
   npm run dev
   ```

4. **Open in Browser**:
   Visit http://localhost:3000

## Pages

- `/` - Home page with search
- `/discover` - Place discovery with maps
- `/about` - About the application

## Components

- `Header` - Navigation and search
- `PlaceCard` - Individual place display
- `GoogleMap` - Interactive map component
- `DirectionsModal` - Directions display

## Development

- **Build**: `npm run build`
- **Lint**: `npm run lint`
- **Type Check**: `npm run type-check`

## Backend Integration

The frontend connects to the backend API at `http://localhost:8000` for:
- Place search and filtering
- Directions and navigation
- Place details and recommendations