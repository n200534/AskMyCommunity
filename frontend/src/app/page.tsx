'use client';

import { useState } from 'react';
import { MagnifyingGlassIcon, MapPinIcon, StarIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid';

export default function Home() {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = () => {
    if (searchQuery.trim()) {
      // Navigate to discover page with search query
      window.location.href = `/discover?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const samplePlaces = [
    {
      name: 'Blue Tokai Coffee',
      type: 'Cafe',
      rating: 4.8,
      price: '₹₹',
      distance: '0.5 km',
      description: 'Cozy rooftop cafe with amazing city views and great coffee',
    },
    {
      name: 'Cubbon Park',
      type: 'Park',
      rating: 4.7,
      price: 'Free',
      distance: '1.2 km',
      description: 'Perfect for morning walks and weekend picnics',
    },
    {
      name: 'Bangalore Palace',
      type: 'Tourist Attraction',
      rating: 4.6,
      price: '₹₹₹',
      distance: '2.1 km',
      description: 'Historic palace with beautiful architecture and gardens',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Hero Section */}
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Discover Amazing Places
          <span className="block text-blue-600">in Your City</span>
        </h1>
        
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Find the best places, events, and activities in your city with AI-powered recommendations.
        </p>

        {/* Simple Search */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="flex gap-2">
            <div className="relative flex-1">
              <MagnifyingGlassIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask anything... 'Chill rooftop cafe near me'"
                className="w-full pl-12 pr-4 py-4 text-lg text-gray-900 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-8 py-4 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-colors duration-200"
            >
              Search
            </button>
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Try: "Romantic dinner spots", "Weekend activities", "Free events"
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto mb-16">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">10K+</div>
            <div className="text-gray-600">Places</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">50K+</div>
            <div className="text-gray-600">Users</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">95%</div>
            <div className="text-gray-600">Satisfied</div>
          </div>
        </div>
      </div>

      {/* Sample Places */}
      <div className="max-w-6xl mx-auto px-4 pb-20">
        <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
          Popular Places Near You
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {samplePlaces.map((place, index) => (
            <div key={index} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
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
                <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
