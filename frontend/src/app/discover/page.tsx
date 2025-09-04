'use client';

import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon, MapPinIcon, StarIcon, HeartIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';

export default function DiscoverPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [places, setPlaces] = useState([
    {
      id: '1',
      name: 'Blue Tokai Coffee',
      type: 'Cafe',
      rating: 4.8,
      price: '₹₹',
      distance: '0.5 km',
      description: 'Cozy rooftop cafe with amazing city views and great coffee. Perfect for work or casual meetings.',
      isLiked: false,
      likes: 127,
    },
    {
      id: '2',
      name: 'Cubbon Park',
      type: 'Park',
      rating: 4.7,
      price: 'Free',
      distance: '1.2 km',
      description: 'Perfect for morning walks and weekend picnics. Beautiful green space in the heart of the city.',
      isLiked: true,
      likes: 156,
    },
    {
      id: '3',
      name: 'Bangalore Palace',
      type: 'Tourist Attraction',
      rating: 4.6,
      price: '₹₹₹',
      distance: '2.1 km',
      description: 'Historic palace with beautiful architecture and gardens. A must-visit for history enthusiasts.',
      isLiked: false,
      likes: 89,
    },
    {
      id: '4',
      name: 'Toit Brewery',
      type: 'Restaurant',
      rating: 4.5,
      price: '₹₹₹',
      distance: '1.8 km',
      description: 'Famous brewery with great food and craft beer. Perfect for evening hangouts with friends.',
      isLiked: false,
      likes: 203,
    },
    {
      id: '5',
      name: 'Lalbagh Botanical Garden',
      type: 'Garden',
      rating: 4.4,
      price: '₹₹',
      distance: '3.2 km',
      description: 'Beautiful botanical garden with diverse plant species. Great for nature lovers and photography.',
      isLiked: true,
      likes: 98,
    },
    {
      id: '6',
      name: 'Commercial Street',
      type: 'Shopping',
      rating: 4.2,
      price: '₹₹',
      distance: '2.5 km',
      description: 'Famous shopping street with traditional and modern stores. Perfect for street shopping.',
      isLiked: false,
      likes: 145,
    },
  ]);

  // Get search query from URL
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
      setSearchQuery(query);
    }
  }, []);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setIsLoading(true);
      // Simulate API call
      setTimeout(() => {
        setIsLoading(false);
      }, 1000);
    }
  };

  const handleLike = (id: string) => {
    setPlaces(prev => 
      prev.map(place => 
        place.id === id 
          ? { 
              ...place, 
              isLiked: !place.isLiked, 
              likes: place.isLiked ? place.likes - 1 : place.likes + 1 
            }
          : place
      )
    );
  };

  const filteredPlaces = searchQuery 
    ? places.filter(place => 
        place.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        place.type.toLowerCase().includes(searchQuery.toLowerCase()) ||
        place.description.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : places;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Discover Places</h1>
          <p className="text-gray-600">Find amazing places, events, and activities in your city</p>
        </div>

        {/* Simple Search */}
        <div className="mb-8">
          <div className="flex gap-2 max-w-2xl">
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
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
        </div>

        {/* Results */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">
              {isLoading ? 'Searching...' : `${filteredPlaces.length} Places Found`}
            </h2>
            <select className="px-3 py-2 text-gray-900 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option>Sort by Rating</option>
              <option>Sort by Distance</option>
              <option>Sort by Price</option>
            </select>
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPlaces.map((place) => (
                <div key={place.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
                  <div className="h-48 bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center">
                    <MapPinIcon className="h-16 w-16 text-white opacity-50" />
                  </div>
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="text-xl font-semibold text-gray-900">{place.name}</h3>
                      <div className="flex items-center space-x-1">
                        <StarSolidIcon className="h-5 w-5 text-yellow-400" />
                        <span className="text-sm font-medium text-gray-600">{place.rating}</span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">{place.type}</span>
                      <span>{place.price}</span>
                      <span className="flex items-center">
                        <MapPinIcon className="h-4 w-4 mr-1" />
                        {place.distance}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-4">{place.description}</p>
                    <div className="flex items-center justify-between">
                      <button
                        onClick={() => handleLike(place.id)}
                        className={`flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors duration-200 ${
                          place.isLiked
                            ? 'bg-red-100 text-red-600'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                        }`}
                      >
                        {place.isLiked ? (
                          <HeartSolidIcon className="h-4 w-4" />
                        ) : (
                          <HeartIcon className="h-4 w-4" />
                        )}
                        <span className="text-sm font-medium">{place.likes}</span>
                      </button>
                      <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">
                        View Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Load More */}
        {!isLoading && filteredPlaces.length > 0 && (
          <div className="text-center mt-8">
            <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200">
              Load More Places
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
