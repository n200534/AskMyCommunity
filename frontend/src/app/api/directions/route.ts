import { NextRequest, NextResponse } from 'next/server';

// Types
interface DirectionsStep {
  instruction: string;
  distance: string;
  duration: string;
}

interface Directions {
  steps: DirectionsStep[];
  total_distance: string;
  total_duration: string;
  mode: string;
}

// Mock directions data (in production, integrate with Google Maps Directions API)
const MOCK_DIRECTIONS: { [key: string]: Directions } = {
  'default': {
    steps: [
      {
        instruction: "Head north on Main St",
        distance: "0.5 mi",
        duration: "2 min"
      },
      {
        instruction: "Turn right onto Market St",
        distance: "1.2 mi",
        duration: "5 min"
      },
      {
        instruction: "Turn left onto Destination St",
        distance: "0.3 mi",
        duration: "1 min"
      }
    ],
    total_distance: "2.0 mi",
    total_duration: "8 min",
    mode: "driving"
  },
  'walking': {
    steps: [
      {
        instruction: "Start walking north on Main St",
        distance: "0.5 mi",
        duration: "10 min"
      },
      {
        instruction: "Turn right onto Market St",
        distance: "1.2 mi",
        duration: "24 min"
      },
      {
        instruction: "Turn left onto Destination St",
        distance: "0.3 mi",
        duration: "6 min"
      }
    ],
    total_distance: "2.0 mi",
    total_duration: "40 min",
    mode: "walking"
  },
  'transit': {
    steps: [
      {
        instruction: "Walk to Main St Station (2 min)",
        distance: "0.1 mi",
        duration: "2 min"
      },
      {
        instruction: "Take Metro Line 1 towards Downtown",
        distance: "1.5 mi",
        duration: "8 min"
      },
      {
        instruction: "Transfer to Bus 15 at Market St",
        distance: "0.3 mi",
        duration: "5 min"
      },
      {
        instruction: "Walk to destination",
        distance: "0.1 mi",
        duration: "2 min"
      }
    ],
    total_distance: "2.0 mi",
    total_duration: "17 min",
    mode: "transit"
  }
};

// Generate directions based on coordinates and mode
function generateDirections(
  originLat: number,
  originLng: number,
  destLat: number,
  destLng: number,
  mode: string = 'driving'
): Directions {
  // Calculate approximate distance
  const distance = calculateDistance(originLat, originLng, destLat, destLng);
  
  // Get base directions for the mode
  const baseDirections = MOCK_DIRECTIONS[mode] || MOCK_DIRECTIONS['default'];
  
  // Adjust distances and durations based on actual distance
  const scaleFactor = Math.max(0.5, Math.min(2.0, distance / 2.0)); // Scale between 0.5x and 2x
  
  const adjustedSteps = baseDirections.steps.map(step => ({
    ...step,
    distance: `${(parseFloat(step.distance) * scaleFactor).toFixed(1)} mi`,
    duration: adjustDuration(step.duration, scaleFactor, mode)
  }));

  return {
    steps: adjustedSteps,
    total_distance: `${(distance * scaleFactor).toFixed(1)} mi`,
    total_duration: adjustDuration(baseDirections.total_duration, scaleFactor, mode),
    mode
  };
}

// Calculate distance between two points (Haversine formula)
function calculateDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng/2) * Math.sin(dLng/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}

// Adjust duration based on distance and mode
function adjustDuration(originalDuration: string, scaleFactor: number, mode: string): string {
  const minutes = parseInt(originalDuration.replace(/\D/g, ''));
  const adjustedMinutes = Math.round(minutes * scaleFactor);
  
  if (adjustedMinutes < 60) {
    return `${adjustedMinutes} min`;
  } else {
    const hours = Math.floor(adjustedMinutes / 60);
    const remainingMinutes = adjustedMinutes % 60;
    return remainingMinutes > 0 ? `${hours}h ${remainingMinutes}m` : `${hours}h`;
  }
}

// API Route Handler
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { 
      origin_lat, 
      origin_lng, 
      destination_lat, 
      destination_lng, 
      mode = 'driving' 
    } = body;

    // Validate required parameters
    if (origin_lat === undefined || origin_lng === undefined || 
        destination_lat === undefined || destination_lng === undefined) {
      return NextResponse.json(
        { error: 'Origin and destination coordinates are required' },
        { status: 400 }
      );
    }

    // Validate mode
    const validModes = ['driving', 'walking', 'transit', 'bicycling'];
    if (!validModes.includes(mode)) {
      return NextResponse.json(
        { error: 'Invalid mode. Must be one of: driving, walking, transit, bicycling' },
        { status: 400 }
      );
    }

    const directions = generateDirections(
      origin_lat, 
      origin_lng, 
      destination_lat, 
      destination_lng, 
      mode
    );

    return NextResponse.json(directions);
  } catch (error) {
    console.error('Directions API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// GET endpoint for testing
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const originLat = parseFloat(searchParams.get('origin_lat') || '37.7749');
  const originLng = parseFloat(searchParams.get('origin_lng') || '-122.4194');
  const destLat = parseFloat(searchParams.get('dest_lat') || '37.7849');
  const destLng = parseFloat(searchParams.get('dest_lng') || '-122.4094');
  const mode = searchParams.get('mode') || 'driving';

  try {
    const directions = generateDirections(originLat, originLng, destLat, destLng, mode);
    return NextResponse.json(directions);
  } catch (error) {
    console.error('Directions API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
