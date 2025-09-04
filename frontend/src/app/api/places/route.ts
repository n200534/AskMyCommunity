import { NextRequest, NextResponse } from 'next/server';
import axios from 'axios';
import * as cheerio from 'cheerio';

// Types
interface Place {
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
}

interface SearchResponse {
  places: Place[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  query: string;
}

// Web scraping sources
const BLOG_SOURCES = [
  {
    name: 'Time Out',
    baseUrl: 'https://www.timeout.com',
    searchUrl: 'https://www.timeout.com/search?q=',
    selectors: {
      container: '.card',
      title: '.card__title',
      description: '.card__description',
      link: '.card__link',
      image: '.card__image img'
    }
  },
  {
    name: 'Lonely Planet',
    baseUrl: 'https://www.lonelyplanet.com',
    searchUrl: 'https://www.lonelyplanet.com/search?q=',
    selectors: {
      container: '.search-result',
      title: '.search-result__title',
      description: '.search-result__description',
      link: '.search-result__link',
      image: '.search-result__image img'
    }
  },
  {
    name: 'TripAdvisor',
    baseUrl: 'https://www.tripadvisor.com',
    searchUrl: 'https://www.tripadvisor.com/search?q=',
    selectors: {
      container: '.result',
      title: '.result-title',
      description: '.result-description',
      link: '.result-title a',
      image: '.result-image img'
    }
  }
];

// Mock coordinates for different cities
const CITY_COORDINATES = {
  'san francisco': { lat: 37.7749, lng: -122.4194 },
  'new york': { lat: 40.7128, lng: -74.0060 },
  'london': { lat: 51.5074, lng: -0.1278 },
  'paris': { lat: 48.8566, lng: 2.3522 },
  'tokyo': { lat: 35.6762, lng: 139.6503 },
  'default': { lat: 37.7749, lng: -122.4194 }
};

// Scrape a single blog source
async function scrapeBlogSource(source: any, query: string): Promise<Place[]> {
  try {
    const searchUrl = `${source.searchUrl}${encodeURIComponent(query)}`;
    console.log(`Scraping ${source.name}: ${searchUrl}`);
    
    const response = await axios.get(searchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      },
      timeout: 10000
    });

    const $ = cheerio.load(response.data);
    const places: Place[] = [];

    $(source.selectors.container).each((index, element) => {
      try {
        const title = $(element).find(source.selectors.title).text().trim();
        const description = $(element).find(source.selectors.description).text().trim();
        const link = $(element).find(source.selectors.link).attr('href');
        const image = $(element).find(source.selectors.image).attr('src');

        if (title && description) {
          // Generate coordinates based on city or use default
          const city = query.toLowerCase().includes('san francisco') ? 'san francisco' :
                      query.toLowerCase().includes('new york') ? 'new york' :
                      query.toLowerCase().includes('london') ? 'london' :
                      query.toLowerCase().includes('paris') ? 'paris' :
                      query.toLowerCase().includes('tokyo') ? 'tokyo' : 'default';
          
          const coords = CITY_COORDINATES[city as keyof typeof CITY_COORDINATES] || CITY_COORDINATES.default;

          places.push({
            id: `${source.name.toLowerCase()}-${index}`,
            name: title,
            address: description,
            latitude: coords.lat + (Math.random() - 0.5) * 0.01, // Add some randomness
            longitude: coords.lng + (Math.random() - 0.5) * 0.01,
            rating: 4.0 + Math.random() * 1.0, // Random rating between 4.0-5.0
            price_level: Math.floor(Math.random() * 4), // 0-3 price levels
            place_type: extractPlaceType(query, title, description),
            photo_url: image ? (image.startsWith('http') ? image : `${source.baseUrl}${image}`) : undefined,
            website: link ? (link.startsWith('http') ? link : `${source.baseUrl}${link}`) : undefined,
            description: description,
            source: source.name
          });
        }
      } catch (error) {
        console.error(`Error parsing item ${index} from ${source.name}:`, error);
      }
    });

    console.log(`Found ${places.length} places from ${source.name}`);
    return places;
  } catch (error) {
    console.error(`Error scraping ${source.name}:`, error);
    return [];
  }
}

// Extract place type from query and content
function extractPlaceType(query: string, title: string, description: string): string {
  const text = `${query} ${title} ${description}`.toLowerCase();
  
  if (text.includes('restaurant') || text.includes('food') || text.includes('dining')) return 'restaurant';
  if (text.includes('cafe') || text.includes('coffee')) return 'cafe';
  if (text.includes('hotel') || text.includes('accommodation')) return 'hotel';
  if (text.includes('museum') || text.includes('gallery')) return 'museum';
  if (text.includes('park') || text.includes('garden')) return 'park';
  if (text.includes('bar') || text.includes('pub')) return 'bar';
  if (text.includes('shop') || text.includes('store')) return 'shop';
  if (text.includes('attraction') || text.includes('sight')) return 'attraction';
  
  return 'place';
}

// Main search function
async function searchPlaces(query: string, page: number = 1, pageSize: number = 20): Promise<SearchResponse> {
  console.log(`Searching for: "${query}"`);
  
  // Scrape all blog sources in parallel
  const scrapePromises = BLOG_SOURCES.map(source => scrapeBlogSource(source, query));
  const results = await Promise.all(scrapePromises);
  
  // Combine and deduplicate results
  const allPlaces = results.flat();
  const uniquePlaces = allPlaces.filter((place, index, self) => 
    index === self.findIndex(p => p.name.toLowerCase() === place.name.toLowerCase())
  );

  // Apply pagination
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const paginatedPlaces = uniquePlaces.slice(startIndex, endIndex);
  
  const totalPages = Math.ceil(uniquePlaces.length / pageSize);

  return {
    places: paginatedPlaces,
    total: uniquePlaces.length,
    page,
    page_size: pageSize,
    total_pages: totalPages,
    query
  };
}

// API Route Handler
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query, page = 1, page_size = 20 } = body;

    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter is required' },
        { status: 400 }
      );
    }

    const results = await searchPlaces(query, page, page_size);
    
    return NextResponse.json(results);
  } catch (error) {
    console.error('Search API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// GET endpoint for testing
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('q') || 'coffee shops';
  const page = parseInt(searchParams.get('page') || '1');
  const pageSize = parseInt(searchParams.get('page_size') || '10');

  try {
    const results = await searchPlaces(query, page, pageSize);
    return NextResponse.json(results);
  } catch (error) {
    console.error('Search API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
