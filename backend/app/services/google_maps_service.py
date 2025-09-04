"""
Google Maps Service for Places and Directions
"""

import httpx
from typing import List, Dict, Any, Optional, Tuple
import json
from ..core.config import settings


class GoogleMapsService:
    """Google Maps service for places search and directions"""
    
    def __init__(self):
        self.api_key = settings.google_maps_api_key
        self.base_url = "https://maps.googleapis.com/maps/api"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_places(
        self,
        query: str,
        location: Optional[Tuple[float, float]] = None,
        radius: Optional[int] = None,
        place_type: Optional[str] = None,
        price_level: Optional[int] = None,
        min_rating: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for places using Google Places API
        """
        params = {
            "query": query,
            "key": self.api_key,
            "fields": "place_id,name,formatted_address,geometry,rating,price_level,types,photos,opening_hours,formatted_phone_number,website,reviews"
        }
        
        if location:
            params["location"] = f"{location[0]},{location[1]}"
        
        if radius:
            params["radius"] = radius
        
        if place_type:
            params["type"] = place_type
        
        try:
            response = await self.client.get(
                f"{self.base_url}/place/textsearch/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise Exception(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
            
            places = []
            for place in data.get("results", []):
                place_data = await self._format_place_data(place)
                places.append(place_data)
            
            return places
            
        except Exception as e:
            print(f"Google Places API error: {e}")
            return []
    
    async def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific place
        """
        params = {
            "place_id": place_id,
            "key": self.api_key,
            "fields": "place_id,name,formatted_address,geometry,rating,price_level,types,photos,opening_hours,formatted_phone_number,website,reviews,editorial_summary"
        }
        
        try:
            response = await self.client.get(
                f"{self.base_url}/place/details/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise Exception(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
            
            result = data.get("result", {})
            return await self._format_place_data(result, detailed=True)
            
        except Exception as e:
            print(f"Google Places API error: {e}")
            return None
    
    async def get_directions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        mode: str = "driving"
    ) -> Optional[Dict[str, Any]]:
        """
        Get directions between two points
        """
        params = {
            "origin": f"{origin[0]},{origin[1]}",
            "destination": f"{destination[0]},{destination[1]}",
            "mode": mode,  # driving, walking, bicycling, transit
            "key": self.api_key
        }
        
        try:
            response = await self.client.get(
                f"{self.base_url}/directions/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise Exception(f"Google Directions API error: {data.get('error_message', 'Unknown error')}")
            
            routes = data.get("routes", [])
            if not routes:
                return None
            
            route = routes[0]
            legs = route.get("legs", [])
            if not legs:
                return None
            
            leg = legs[0]
            
            return {
                "distance": leg.get("distance", {}).get("text", ""),
                "duration": leg.get("duration", {}).get("text", ""),
                "start_address": leg.get("start_address", ""),
                "end_address": leg.get("end_address", ""),
                "steps": [
                    {
                        "instruction": step.get("html_instructions", ""),
                        "distance": step.get("distance", {}).get("text", ""),
                        "duration": step.get("duration", {}).get("text", "")
                    }
                    for step in leg.get("steps", [])
                ],
                "overview_polyline": route.get("overview_polyline", {}).get("points", "")
            }
            
        except Exception as e:
            print(f"Google Directions API error: {e}")
            return None
    
    async def get_nearby_places(
        self,
        location: Tuple[float, float],
        radius: int = 1000,
        place_type: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get nearby places using Google Places Nearby Search
        """
        params = {
            "location": f"{location[0]},{location[1]}",
            "radius": radius,
            "key": self.api_key,
            "fields": "place_id,name,formatted_address,geometry,rating,price_level,types,photos,opening_hours,formatted_phone_number,website"
        }
        
        if place_type:
            params["type"] = place_type
        
        if keyword:
            params["keyword"] = keyword
        
        try:
            response = await self.client.get(
                f"{self.base_url}/place/nearbysearch/json",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "OK":
                raise Exception(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
            
            places = []
            for place in data.get("results", []):
                place_data = await self._format_place_data(place)
                places.append(place_data)
            
            return places
            
        except Exception as e:
            print(f"Google Places API error: {e}")
            return []
    
    async def _format_place_data(self, place: Dict[str, Any], detailed: bool = False) -> Dict[str, Any]:
        """
        Format Google Places data to our standard format
        """
        geometry = place.get("geometry", {})
        location = geometry.get("location", {})
        
        # Get photo URL if available
        photo_url = None
        photos = place.get("photos", [])
        if photos:
            photo_reference = photos[0].get("photo_reference")
            if photo_reference:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={self.api_key}"
        
        # Format opening hours
        opening_hours = place.get("opening_hours", {})
        hours_text = opening_hours.get("weekday_text", [])
        
        # Format reviews
        reviews = []
        if detailed:
            for review in place.get("reviews", []):
                reviews.append({
                    "author_name": review.get("author_name", ""),
                    "rating": review.get("rating", 0),
                    "text": review.get("text", ""),
                    "time": review.get("time", 0)
                })
        
        # Determine place type from Google types
        google_types = place.get("types", [])
        place_type = self._map_google_types(google_types)
        
        # Map price level to our format
        price_level = place.get("price_level", 0)
        price_range = self._map_price_level(price_level)
        
        return {
            "google_place_id": place.get("place_id"),
            "name": place.get("name", ""),
            "description": place.get("editorial_summary", {}).get("overview", "") if detailed else "",
            "place_type": place_type,
            "address": place.get("formatted_address", ""),
            "latitude": location.get("lat"),
            "longitude": location.get("lng"),
            "rating": place.get("rating", 0.0),
            "price_range": price_range,
            "phone": place.get("formatted_phone_number", ""),
            "website": place.get("website", ""),
            "opening_hours": json.dumps({
                "weekday_text": hours_text,
                "open_now": opening_hours.get("open_now", False)
            }),
            "amenities": json.dumps(google_types),
            "images": json.dumps([photo_url] if photo_url else []),
            "is_verified": True,  # Google places are verified
            "is_active": True,
            "reviews": reviews if detailed else [],
            "user_ratings_total": place.get("user_ratings_total", 0)
        }
    
    def _map_google_types(self, google_types: List[str]) -> str:
        """
        Map Google Places types to our place types
        """
        type_mapping = {
            "restaurant": "restaurant",
            "cafe": "cafe",
            "bar": "bar",
            "park": "park",
            "museum": "museum",
            "shopping_mall": "shopping",
            "store": "shopping",
            "tourist_attraction": "tourist_attraction",
            "gym": "fitness",
            "beauty_salon": "beauty",
            "hospital": "health",
            "university": "education",
            "movie_theater": "entertainment",
            "amusement_park": "entertainment"
        }
        
        for google_type in google_types:
            if google_type in type_mapping:
                return type_mapping[google_type]
        
        return "other"
    
    def _map_price_level(self, price_level: int) -> str:
        """
        Map Google price level to our price range format
        """
        price_mapping = {
            0: "Free",
            1: "$",
            2: "$$",
            3: "$$$",
            4: "$$$$"
        }
        
        return price_mapping.get(price_level, "$$")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global Google Maps service instance
google_maps_service = GoogleMapsService()
