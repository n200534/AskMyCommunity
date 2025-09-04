'use client';

import { useEffect, useRef, useState } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
import { Place } from '@/lib/maps';

interface GoogleMapProps {
  places: Place[];
  selectedPlace?: Place | null;
  onPlaceSelect?: (place: Place) => void;
  center?: { lat: number; lng: number };
  zoom?: number;
  className?: string;
}

export default function GoogleMap({
  places,
  selectedPlace,
  onPlaceSelect,
  center = { lat: 12.9716, lng: 77.5946 }, // Default to Bangalore
  zoom = 13,
  className = 'h-96 w-full'
}: GoogleMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<google.maps.Map | null>(null);
  const markersRef = useRef<google.maps.Marker[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initMap = async () => {
      try {
        const loader = new Loader({
          apiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || '',
          version: 'weekly',
          libraries: ['places', 'geometry']
        });

        const { Map } = await loader.importLibrary('maps');

        if (mapRef.current) {
          const map = new Map(mapRef.current, {
            center,
            zoom,
            mapTypeControl: true,
            streetViewControl: false,
            fullscreenControl: true,
            zoomControl: true,
          });

          mapInstanceRef.current = map;
          setIsLoaded(true);
        }
      } catch (err) {
        setError('Failed to load Google Maps');
        console.error('Error loading Google Maps:', err);
      }
    };

    initMap();
  }, []);

  useEffect(() => {
    if (!isLoaded || !mapInstanceRef.current) return;

    const map = mapInstanceRef.current;
    
    // Clear existing markers
    markersRef.current.forEach(marker => marker.setMap(null));
    markersRef.current = [];

    // Add markers for places
    places.forEach((place) => {
      if (place.latitude && place.longitude) {
        const marker = new google.maps.Marker({
          position: { lat: place.latitude, lng: place.longitude },
          map,
          title: place.name,
          icon: {
            url: selectedPlace?.id === place.id 
              ? 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="16" cy="16" r="12" fill="#3B82F6" stroke="#1E40AF" stroke-width="2"/>
                  <circle cx="16" cy="16" r="6" fill="white"/>
                </svg>
              `)
              : 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(`
                <svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="8" fill="#EF4444" stroke="#DC2626" stroke-width="2"/>
                  <circle cx="12" cy="12" r="4" fill="white"/>
                </svg>
              `),
            scaledSize: new google.maps.Size(32, 32),
            anchor: new google.maps.Point(16, 16),
          },
        });

        // Add click listener
        marker.addListener('click', () => {
          if (onPlaceSelect) {
            onPlaceSelect(place);
          }
        });

        // Add info window
        const infoWindow = new google.maps.InfoWindow({
          content: `
            <div class="p-2">
              <h3 class="font-semibold text-gray-900">${place.name}</h3>
              <p class="text-sm text-gray-600">${place.place_type}</p>
              <p class="text-sm text-gray-500">${place.address}</p>
              <div class="flex items-center mt-1">
                <span class="text-yellow-500">★</span>
                <span class="text-sm ml-1">${place.rating.toFixed(1)}</span>
                <span class="text-sm text-gray-500 ml-2">${'$'.repeat(place.price_level)}</span>
              </div>
            </div>
          `,
        });

        marker.addListener('click', () => {
          infoWindow.open(map, marker);
        });

        markersRef.current.push(marker);
      }
    });

    // Fit map to show all markers
    if (places.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      places.forEach(place => {
        if (place.latitude && place.longitude) {
          bounds.extend({ lat: place.latitude, lng: place.longitude });
        }
      });
      map.fitBounds(bounds);
    }
  }, [places, selectedPlace, onPlaceSelect, isLoaded, center, zoom]);

  if (error) {
    return (
      <div className={`${className} flex items-center justify-center bg-gray-100 rounded-lg`}>
        <div className="text-center">
          <p className="text-red-600 mb-2">Failed to load map</p>
          <p className="text-sm text-gray-500">{error}</p>
        </div>
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className={`${className} flex items-center justify-center bg-gray-100 rounded-lg`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
          <p className="text-gray-600">Loading map...</p>
        </div>
      </div>
    );
  }

  return <div ref={mapRef} className={className} />;
}
