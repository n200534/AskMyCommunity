// Google Maps API configuration and utilities

export const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '';

export interface Place {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  rating: number;
  price_level: number;
  place_type: string;
  photo_url?: string;
  phone?: string;
  website?: string;
  opening_hours?: string[];
  description?: string;
  source: string;
  distance?: number;
}

export interface Directions {
  distance: string;
  duration: string;
  start_address: string;
  end_address: string;
  steps: Array<{
    instruction: string;
    distance: string;
    duration: string;
  }>;
  overview_polyline: string;
}

export interface SearchRequest {
  query: string;
  place_type?: string;
  min_rating?: number;
  max_price?: string;
  latitude?: number;
  longitude?: number;
  radius?: number;
  page: number;
  page_size: number;
  sort_by: 'relevance' | 'rating' | 'distance' | 'price';
}

export interface SearchResponse {
  places: Place[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  query: string;
  filters_applied: Record<string, unknown>;
}

// API functions
export async function searchPlaces(searchRequest: SearchRequest): Promise<SearchResponse> {
  const response = await fetch('/api/places', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(searchRequest),
  });

  if (!response.ok) {
    throw new Error('Failed to search places');
  }

  return response.json();
}

export async function getNearbyPlaces(
  latitude: number,
  longitude: number,
  radius: number = 1000,
  placeType?: string,
  keyword?: string
): Promise<Place[]> {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    radius: radius.toString(),
  });

  if (placeType) params.append('place_type', placeType);
  if (keyword) params.append('keyword', keyword);

  const response = await fetch(`/api/v1/maps/nearby?${params}`);

  if (!response.ok) {
    throw new Error('Failed to get nearby places');
  }

  return response.json();
}

export async function getPlaceDetails(placeId: string): Promise<Place> {
  const response = await fetch(`/api/v1/maps/place/${placeId}`);

  if (!response.ok) {
    throw new Error('Failed to get place details');
  }

  return response.json();
}

export async function getDirections(
  originLat: number,
  originLng: number,
  destLat: number,
  destLng: number,
  mode: string = 'driving'
): Promise<Directions> {
  const params = new URLSearchParams({
    origin_lat: originLat.toString(),
    origin_lng: originLng.toString(),
    dest_lat: destLat.toString(),
    dest_lng: destLng.toString(),
    mode,
  });

  const response = await fetch(`/api/directions?${params}`);

  if (!response.ok) {
    throw new Error('Failed to get directions');
  }

  return response.json();
}

// Utility functions
export function formatDistance(distance: number): string {
  if (distance < 1) {
    return `${Math.round(distance * 1000)}m`;
  }
  return `${distance.toFixed(1)}km`;
}

export function formatRating(rating: number): string {
  return rating.toFixed(1);
}

export function getPriceRangeDisplay(priceRange: string): string {
  const priceMap: Record<string, string> = {
    'Free': 'Free',
    '$': 'Budget',
    '$$': 'Moderate',
    '$$$': 'Expensive',
    '$$$$': 'Very Expensive',
  };
  return priceMap[priceRange] || priceRange;
}

export function getPlaceTypeDisplay(placeType: string): string {
  return placeType
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
