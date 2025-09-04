'use client';

import { useState } from 'react';
import Image from 'next/image';
import { MapPinIcon, HeartIcon, PhoneIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import { Place, formatDistance, formatRating, getPriceRangeDisplay, getPlaceTypeDisplay } from '@/lib/maps';

interface AIRecommendation {
  confidence: number;
  reasoning: string;
  personalized_notes: string;
  best_for: string[];
  avoid_if: string[];
  best_time_to_visit: string;
  local_tips: string[];
}

interface EnhancedPlace extends Place {
  ai_recommendation?: AIRecommendation;
  ai_confidence?: number;
  ai_rank?: number;
}

interface PlaceCardProps {
  place: EnhancedPlace;
  onSelect?: (place: EnhancedPlace) => void;
  onLike?: (place: EnhancedPlace) => void;
  onGetDirections?: (place: EnhancedPlace) => void;
  isSelected?: boolean;
}

export default function PlaceCard({
  place,
  onSelect,
  onLike,
  onGetDirections,
  isSelected = false
}: PlaceCardProps) {
  const [isLiked, setIsLiked] = useState(false);
  const [imageError, setImageError] = useState(false);

  const handleLike = () => {
    setIsLiked(!isLiked);
    if (onLike) {
      onLike(place);
    }
  };

  const handleSelect = () => {
    if (onSelect) {
      onSelect(place);
    }
  };

  const handleGetDirections = () => {
    if (onGetDirections) {
      onGetDirections(place);
    }
  };

  return (
    <div 
      className={`bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer ${
        isSelected ? 'ring-2 ring-blue-500' : ''
      }`}
      onClick={handleSelect}
    >
      {/* Image */}
      <div className="h-48 bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center relative">
        {place.photo_url && !imageError ? (
          <Image
            src={place.photo_url}
            alt={place.name}
            fill
            className="object-cover"
            onError={() => setImageError(true)}
          />
        ) : (
          <MapPinIcon className="h-16 w-16 text-white opacity-50" />
        )}
        
        {/* AI Badge */}
        {place.ai_confidence && place.ai_confidence > 0.8 && (
          <div className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
            AI Recommended
          </div>
        )}
        
        {/* Like Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleLike();
          }}
          className="absolute top-2 left-2 p-2 bg-white bg-opacity-20 rounded-full hover:bg-opacity-30 transition-colors"
        >
          {isLiked ? (
            <HeartSolidIcon className="h-5 w-5 text-red-500" />
          ) : (
            <HeartIcon className="h-5 w-5 text-white" />
          )}
        </button>
      </div>

      {/* Content */}
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <h3 className="text-xl font-semibold text-gray-900 mb-1">{place.name}</h3>
            <p className="text-sm text-gray-600 capitalize">
              {getPlaceTypeDisplay(place.place_type)}
            </p>
          </div>
          <div className="flex items-center space-x-1 ml-2">
            <StarSolidIcon className="h-5 w-5 text-yellow-400" />
            <span className="text-sm font-medium text-gray-600">
              {formatRating(place.rating)}
            </span>
          </div>
        </div>


        {/* Description */}
        {place.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {place.description}
          </p>
        )}

        {/* AI Recommendation */}
        {place.ai_recommendation && (
          <div className="mb-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-blue-700 uppercase tracking-wide">
                AI Recommendation
              </span>
              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                {place.ai_confidence}% match
              </span>
            </div>
            <p className="text-sm text-gray-700 mb-2">{place.ai_recommendation.reasoning}</p>
            
            {place.ai_recommendation.best_for && place.ai_recommendation.best_for.length > 0 && (
              <div className="mb-2">
                <span className="text-xs font-medium text-green-700">Best for:</span>
                <div className="flex flex-wrap gap-1 mt-1">
                  {place.ai_recommendation.best_for.slice(0, 3).map((item, index) => (
                    <span key={index} className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {place.ai_recommendation.local_tips && place.ai_recommendation.local_tips.length > 0 && (
              <div>
                <span className="text-xs font-medium text-purple-700">Local tip:</span>
                <p className="text-xs text-gray-600 mt-1">{place.ai_recommendation.local_tips[0]}</p>
              </div>
            )}
          </div>
        )}

        {/* Details */}
        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
            {getPriceRangeDisplay(place.price_level.toString())}
          </span>
          {place.distance && (
            <span className="flex items-center">
              <MapPinIcon className="h-4 w-4 mr-1" />
              {formatDistance(place.distance)}
            </span>
          )}
          <span>Reviews available</span>
        </div>

        {/* Address */}
        <p className="text-sm text-gray-500 mb-4">{place.address}</p>

        {/* Contact Info */}
        {(place.phone || place.website) && (
          <div className="flex items-center space-x-4 mb-4">
            {place.phone && (
              <a
                href={`tel:${place.phone}`}
                onClick={(e) => e.stopPropagation()}
                className="flex items-center text-sm text-blue-600 hover:text-blue-800"
              >
                <PhoneIcon className="h-4 w-4 mr-1" />
                Call
              </a>
            )}
            {place.website && (
              <a
                href={place.website}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="flex items-center text-sm text-blue-600 hover:text-blue-800"
              >
                <GlobeAltIcon className="h-4 w-4 mr-1" />
                Website
              </a>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="flex space-x-2">
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleGetDirections();
            }}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
          >
            Get Directions
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              // Handle view details
            }}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm"
          >
            View Details
          </button>
        </div>
      </div>
    </div>
  );
}
