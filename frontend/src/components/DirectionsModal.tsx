'use client';

import { useState, useEffect } from 'react';
import { XMarkIcon, MapPinIcon, ClockIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import { getDirections, Directions } from '@/lib/maps';

interface DirectionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  origin: { lat: number; lng: number; address?: string };
  destination: { lat: number; lng: number; address?: string };
  mode?: string;
}

export default function DirectionsModal({
  isOpen,
  onClose,
  origin,
  destination,
  mode = 'driving'
}: DirectionsModalProps) {
  const [directions, setDirections] = useState<Directions | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && origin && destination) {
      loadDirections();
    }
  }, [isOpen, origin, destination, mode]);

  const loadDirections = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await getDirections(
        origin.lat,
        origin.lng,
        destination.lat,
        destination.lng,
        mode
      );
      setDirections(result);
    } catch (err) {
      setError('Failed to load directions');
      console.error('Error loading directions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-semibold text-gray-900">Directions</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-3 text-gray-600">Loading directions...</span>
            </div>
          )}

          {error && (
            <div className="text-center py-8">
              <p className="text-red-600 mb-4">{error}</p>
              <button
                onClick={loadDirections}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          )}

          {directions && (
            <div className="space-y-6">
              {/* Summary */}
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center">
                    <MapPinIcon className="h-5 w-5 text-green-600 mr-2" />
                    <span className="font-medium text-gray-900">From</span>
                  </div>
                  <div className="flex items-center">
                    <MapPinIcon className="h-5 w-5 text-red-600 mr-2" />
                    <span className="font-medium text-gray-900">To</span>
                  </div>
                </div>
                <div className="text-sm text-gray-600 mb-3">
                  <p>{directions.start_address}</p>
                  <p className="mt-1">{directions.end_address}</p>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <ClockIcon className="h-4 w-4 text-gray-500 mr-1" />
                    <span className="font-medium">{directions.duration}</span>
                  </div>
                  <div className="text-gray-500">
                    {directions.distance}
                  </div>
                </div>
              </div>

              {/* Steps */}
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Step-by-step directions</h3>
                <div className="space-y-3">
                  {directions.steps.map((step, index) => (
                    <div key={index} className="flex items-start">
                      <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white text-xs rounded-full flex items-center justify-center mr-3 mt-0.5">
                        {index + 1}
                      </div>
                      <div className="flex-1">
                        <div 
                          className="text-sm text-gray-900"
                          dangerouslySetInnerHTML={{ __html: step.instruction }}
                        />
                        <div className="flex items-center mt-1 text-xs text-gray-500">
                          <span>{step.distance}</span>
                          <ArrowRightIcon className="h-3 w-3 mx-2" />
                          <span>{step.duration}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-3 pt-4 border-t">
                <button
                  onClick={() => window.open(`https://www.google.com/maps/dir/${origin.lat},${origin.lng}/${destination.lat},${destination.lng}`, '_blank')}
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Open in Google Maps
                </button>
                <button
                  onClick={onClose}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
