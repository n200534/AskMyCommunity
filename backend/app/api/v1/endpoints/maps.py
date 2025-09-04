from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
import math

from ....core.database import get_db
from ....services.google_maps_service import google_maps_service
from ....services.ai_factory import ai_factory
from ....schemas.place import PlaceSearchRequest, PlaceSearchResponse, PlaceWithStats

router = APIRouter()


@router.post("/search", response_model=PlaceSearchResponse)
async def search_places_with_maps(
    search_request: PlaceSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search places using Google Maps API with AI recommendations
    """
    try:
        # Prepare location for Google Maps search
        location = None
        if search_request.latitude and search_request.longitude:
            location = (search_request.latitude, search_request.longitude)
        
        # Search Google Maps for places
        google_places = await google_maps_service.search_places(
            query=search_request.query,
            location=location,
            radius=search_request.radius * 1000 if search_request.radius else 5000,  # Convert km to meters
            place_type=search_request.place_type,
            price_level=search_request.max_price.count('$') if search_request.max_price else None,
            min_rating=search_request.min_rating
        )
        
        if not google_places:
            return PlaceSearchResponse(
                places=[],
                total=0,
                page=search_request.page,
                page_size=search_request.page_size,
                total_pages=0,
                query=search_request.query,
                filters_applied={}
            )
        
        # Use AI to rank and recommend places
        ai_recommendations = await ai_factory.generate_recommendations(
            query=search_request.query,
            available_places=google_places,
            limit=len(google_places)
        )
        
        # Create a mapping of place_id to AI recommendation
        ai_scores = {rec['place_id']: rec for rec in ai_recommendations}
        
        # Format places with AI recommendations
        result_places = []
        for place in google_places:
            place_dict = place.copy()
            
            # Add AI recommendation data if available
            ai_rec = ai_scores.get(place.get('google_place_id'))
            if ai_rec:
                place_dict['ai_confidence'] = ai_rec.get('confidence_score', 0.0)
                place_dict['ai_reason'] = ai_rec.get('reason', '')
                place_dict['ai_rank'] = ai_rec.get('rank', 0)
            
            # Calculate distance if location provided
            distance = None
            if search_request.latitude and search_request.longitude and place.get('latitude') and place.get('longitude'):
                distance = calculate_distance(
                    search_request.latitude, search_request.longitude,
                    place['latitude'], place['longitude']
                )
            
            place_dict['distance'] = distance
            place_dict['review_count'] = place.get('user_ratings_total', 0)
            place_dict['like_count'] = 0  # Will be updated from database if needed
            
            result_places.append(PlaceWithStats(**place_dict))
        
        # Sort by AI rank if available, otherwise by distance or rating
        if search_request.sort_by == "relevance" and any(p.ai_rank for p in result_places):
            result_places.sort(key=lambda x: x.ai_rank or 999)
        elif search_request.sort_by == "distance" and search_request.latitude and search_request.longitude:
            result_places.sort(key=lambda x: x.distance or float('inf'))
        elif search_request.sort_by == "rating":
            result_places.sort(key=lambda x: x.rating, reverse=True)
        
        # Apply pagination
        total = len(result_places)
        start_idx = (search_request.page - 1) * search_request.page_size
        end_idx = start_idx + search_request.page_size
        paginated_places = result_places[start_idx:end_idx]
        
        total_pages = math.ceil(total / search_request.page_size)
        
        return PlaceSearchResponse(
            places=paginated_places,
            total=total,
            page=search_request.page,
            page_size=search_request.page_size,
            total_pages=total_pages,
            query=search_request.query,
            filters_applied={
                "place_type": search_request.place_type,
                "min_rating": search_request.min_rating,
                "max_price": search_request.max_price,
                "radius": search_request.radius
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching places: {str(e)}")


@router.get("/nearby", response_model=List[PlaceWithStats])
async def get_nearby_places(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    radius: int = Query(1000, description="Radius in meters"),
    place_type: Optional[str] = Query(None, description="Place type filter"),
    keyword: Optional[str] = Query(None, description="Keyword search"),
    db: Session = Depends(get_db)
):
    """
    Get nearby places using Google Maps API
    """
    try:
        places = await google_maps_service.get_nearby_places(
            location=(latitude, longitude),
            radius=radius,
            place_type=place_type,
            keyword=keyword
        )
        
        result_places = []
        for place in places:
            # Calculate distance
            distance = calculate_distance(latitude, longitude, place['latitude'], place['longitude'])
            
            place_dict = place.copy()
            place_dict['distance'] = distance
            place_dict['review_count'] = place.get('user_ratings_total', 0)
            place_dict['like_count'] = 0
            
            result_places.append(PlaceWithStats(**place_dict))
        
        return result_places
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting nearby places: {str(e)}")


@router.get("/place/{place_id}", response_model=PlaceWithStats)
async def get_place_details(place_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific place from Google Maps
    """
    try:
        place = await google_maps_service.get_place_details(place_id)
        
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        
        place_dict = place.copy()
        place_dict['review_count'] = place.get('user_ratings_total', 0)
        place_dict['like_count'] = 0
        place_dict['distance'] = None
        
        return PlaceWithStats(**place_dict)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting place details: {str(e)}")


@router.get("/directions")
async def get_directions(
    origin_lat: float = Query(..., description="Origin latitude"),
    origin_lng: float = Query(..., description="Origin longitude"),
    dest_lat: float = Query(..., description="Destination latitude"),
    dest_lng: float = Query(..., description="Destination longitude"),
    mode: str = Query("driving", description="Travel mode: driving, walking, bicycling, transit")
):
    """
    Get directions between two points
    """
    try:
        directions = await google_maps_service.get_directions(
            origin=(origin_lat, origin_lng),
            destination=(dest_lat, dest_lng),
            mode=mode
        )
        
        if not directions:
            raise HTTPException(status_code=404, detail="No directions found")
        
        return directions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting directions: {str(e)}")


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c
