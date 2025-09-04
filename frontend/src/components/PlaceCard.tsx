'use client';

import { useState } from 'react';
import { MapPinIcon, StarIcon, HeartIcon, PhoneIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon, HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';
import { Place, formatDistance, formatRating, getPriceRangeDisplay, getPlaceTypeDisplay } from '@/lib/maps';

interface PlaceCardProps {
  place: Place;
  onSelect?: (place: Place) => void;
  onLike?: (place: Place) => void;
  onGetDirections?: (place: Place) => void;
  isSelected?: boolean;
  showMap?: boolean;
}

export default function PlaceCard({
  place,
  onSelect,
  onLike,
  onGetDirections,
  isSelected = false,
  showMap = false
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
        {place.images && place.images.length > 0 && !imageError ? (
          <img
            src={place.images[0]}
            alt={place.name}
            className="w-full h-full object-cover"
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

        {/* AI Reason */}
        {place.ai_reason && (
          <div className="mb-3 p-2 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">{place.ai_reason}</p>
          </div>
        )}

        {/* Description */}
        {place.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {place.description}
          </p>
        )}

        {/* Details */}
        <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
          <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
            {getPriceRangeDisplay(place.price_range)}
          </span>
          {place.distance && (
            <span className="flex items-center">
              <MapPinIcon className="h-4 w-4 mr-1" />
              {formatDistance(place.distance)}
            </span>
          )}
          <span>{place.review_count} reviews</span>
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
