'use client';

import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, MapPinIcon, StarIcon, HeartIcon, MapIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import GoogleMap from '@/components/GoogleMap';
import PlaceCard from '@/components/PlaceCard';
import DirectionsModal from '@/components/DirectionsModal';
import { searchPlaces, Place, SearchRequest } from '@/lib/maps';

export default function DiscoverPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [places, setPlaces] = useState<Place[]>([]);
  const [selectedPlace, setSelectedPlace] = useState<Place | null>(null);
  const [showMap, setShowMap] = useState(true);
  const [showDirections, setShowDirections] = useState(false);
  const [directionsPlace, setDirectionsPlace] = useState<Place | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);
  const [filters, setFilters] = useState({
    placeType: '',
    minRating: 0,
    maxPrice: '',
    radius: 5
  });

  // Get search query from URL and user location
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
      setSearchQuery(query);
    }

    // Get user location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          // Default to Bangalore
          setUserLocation({ lat: 12.9716, lng: 77.5946 });
        }
      );
    } else {
      // Default to Bangalore
      setUserLocation({ lat: 12.9716, lng: 77.5946 });
    }
  }, []);

  const handleSearch = async () => {
    if (searchQuery.trim()) {
      setIsLoading(true);
      try {
        const searchRequest: SearchRequest = {
          query: searchQuery,
          place_type: filters.placeType || undefined,
          min_rating: filters.minRating || undefined,
          max_price: filters.maxPrice || undefined,
          latitude: userLocation?.lat,
          longitude: userLocation?.lng,
          radius: filters.radius,
          page: 1,
          page_size: 20,
          sort_by: 'relevance'
        };

        const response = await searchPlaces(searchRequest);
        setPlaces(response.places);
      } catch (error) {
        console.error('Error searching places:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handlePlaceSelect = (place: Place) => {
    setSelectedPlace(place);
  };

  const handleGetDirections = (place: Place) => {
    setDirectionsPlace(place);
    setShowDirections(true);
  };

  const handleLike = (place: Place) => {
    // Handle like functionality
    console.log('Liked place:', place.name);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Discover Places</h1>
          <p className="text-gray-600">Find amazing places, events, and activities in your city</p>
        </div>

        {/* Search and Filters */}
        <div className="mb-8">
          <div className="flex gap-2 max-w-2xl mb-4">
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search places, events, activities..."
                className="w-full pl-12 pr-4 py-3 text-lg text-gray-900 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="px-6 py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50"
            >
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-4">
            <select
              value={filters.placeType}
              onChange={(e) => setFilters({...filters, placeType: e.target.value})}
              className="px-3 py-2 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Types</option>
              <option value="restaurant">Restaurant</option>
              <option value="cafe">Cafe</option>
              <option value="park">Park</option>
              <option value="shopping">Shopping</option>
              <option value="entertainment">Entertainment</option>
            </select>

            <select
              value={filters.minRating}
              onChange={(e) => setFilters({...filters, minRating: parseFloat(e.target.value)})}
              className="px-3 py-2 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={0}>All Ratings</option>
              <option value={3}>3+ Stars</option>
              <option value={4}>4+ Stars</option>
              <option value={4.5}>4.5+ Stars</option>
            </select>

            <select
              value={filters.maxPrice}
              onChange={(e) => setFilters({...filters, maxPrice: e.target.value})}
              className="px-3 py-2 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Prices</option>
              <option value="$">Budget ($)</option>
              <option value="$$">Moderate ($$)</option>
              <option value="$$$">Expensive ($$$)</option>
            </select>

            <button
              onClick={() => setShowMap(!showMap)}
              className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <MapIcon className="h-5 w-5 mr-2" />
              {showMap ? 'Hide Map' : 'Show Map'}
            </button>
          </div>
        </div>

        {/* Results */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">
              {isLoading ? 'Searching...' : `${places.length} Places Found`}
            </h2>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-xl shadow-lg overflow-hidden animate-pulse">
                  <div className="h-48 bg-gray-300"></div>
                  <div className="p-6">
                    <div className="h-4 bg-gray-300 rounded mb-2"></div>
                    <div className="h-3 bg-gray-300 rounded mb-4"></div>
                    <div className="h-3 bg-gray-300 rounded"></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Places List */}
              <div className="lg:col-span-2">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {places.map((place) => (
                    <PlaceCard
                      key={place.google_place_id}
                      place={place}
                      onSelect={handlePlaceSelect}
                      onLike={handleLike}
                      onGetDirections={handleGetDirections}
                      isSelected={selectedPlace?.google_place_id === place.google_place_id}
                    />
                  ))}
                </div>
              </div>

              {/* Map */}
              {showMap && (
                <div className="lg:col-span-1">
                  <div className="sticky top-4">
                    <GoogleMap
                      places={places}
                      selectedPlace={selectedPlace}
                      onPlaceSelect={handlePlaceSelect}
                      center={userLocation || { lat: 12.9716, lng: 77.5946 }}
                      className="h-96 w-full rounded-lg"
                    />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Load More */}
        {!isLoading && places.length > 0 && (
          <div className="text-center mt-8">
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200">
              Load More Places
            </button>
          </div>
        )}
      </div>

      {/* Directions Modal */}
      {showDirections && directionsPlace && userLocation && (
        <DirectionsModal
          isOpen={showDirections}
          onClose={() => setShowDirections(false)}
          origin={{
            lat: userLocation.lat,
            lng: userLocation.lng,
            address: 'Your Location'
          }}
          destination={{
            lat: directionsPlace.latitude,
            lng: directionsPlace.longitude,
            address: directionsPlace.address
          }}
        />
      )}
    </div>
  );
}
