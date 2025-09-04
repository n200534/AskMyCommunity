from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from ....core.database import get_db
from ....models.place import Place, Review, PlaceLike
from ....schemas.place import (
    Place as PlaceSchema,
    PlaceCreate,
    PlaceUpdate,
    PlaceSearchRequest,
    PlaceSearchResponse,
    PlaceWithStats
)

router = APIRouter()


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


@router.get("/", response_model=List[PlaceWithStats])
def get_places(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    place_type: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    db: Session = Depends(get_db)
):
    """Get all places with optional filtering"""
    query = db.query(Place).filter(Place.is_active == True)
    
    if place_type:
        query = query.filter(Place.place_type == place_type)
    
    if min_rating:
        query = query.filter(Place.rating >= min_rating)
    
    places = query.offset(skip).limit(limit).all()
    
    # Add stats for each place
    result = []
    for place in places:
        place_dict = place.__dict__.copy()
        
        # Get review count
        review_count = db.query(Review).filter(Review.place_id == place.id).count()
        
        # Get like count
        like_count = db.query(PlaceLike).filter(PlaceLike.place_id == place.id).count()
        
        place_dict.update({
            'review_count': review_count,
            'like_count': like_count
        })
        
        result.append(PlaceWithStats(**place_dict))
    
    return result


@router.get("/{place_id}", response_model=PlaceWithStats)
def get_place(place_id: int, db: Session = Depends(get_db)):
    """Get a specific place by ID"""
    place = db.query(Place).filter(Place.id == place_id, Place.is_active == True).first()
    
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Get stats
    review_count = db.query(Review).filter(Review.place_id == place.id).count()
    like_count = db.query(PlaceLike).filter(PlaceLike.place_id == place.id).count()
    
    place_dict = place.__dict__.copy()
    place_dict.update({
        'review_count': review_count,
        'like_count': like_count
    })
    
    return PlaceWithStats(**place_dict)


@router.post("/search", response_model=PlaceSearchResponse)
def search_places(
    search_request: PlaceSearchRequest,
    db: Session = Depends(get_db)
):
    """Search places with various filters and sorting options"""
    query = db.query(Place).filter(Place.is_active == True)
    
    # Text search
    if search_request.query:
        search_term = f"%{search_request.query.lower()}%"
        query = query.filter(
            Place.name.ilike(search_term) |
            Place.description.ilike(search_term) |
            Place.place_type.ilike(search_term)
        )
    
    # Filters
    if search_request.place_type:
        query = query.filter(Place.place_type == search_request.place_type)
    
    if search_request.min_rating:
        query = query.filter(Place.rating >= search_request.min_rating)
    
    if search_request.max_price:
        query = query.filter(Place.price_range == search_request.max_price)
    
    # Location-based filtering
    if search_request.latitude and search_request.longitude and search_request.radius:
        # This is a simplified approach - in production, use PostGIS or similar
        # For now, we'll just filter by approximate bounding box
        lat_range = search_request.radius / 111.0  # Rough conversion: 1 degree ≈ 111 km
        lon_range = search_request.radius / (111.0 * math.cos(math.radians(search_request.latitude)))
        
        query = query.filter(
            Place.latitude.between(
                search_request.latitude - lat_range,
                search_request.latitude + lat_range
            ),
            Place.longitude.between(
                search_request.longitude - lon_range,
                search_request.longitude + lon_range
            )
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Sorting
    if search_request.sort_by == "rating":
        query = query.order_by(Place.rating.desc())
    elif search_request.sort_by == "price":
        query = query.order_by(Place.price_range.asc())
    else:  # relevance (default)
        query = query.order_by(Place.rating.desc(), Place.name.asc())
    
    # Pagination
    offset = (search_request.page - 1) * search_request.page_size
    places = query.offset(offset).limit(search_request.page_size).all()
    
    # Add stats and calculate distances
    result_places = []
    for place in places:
        place_dict = place.__dict__.copy()
        
        # Get stats
        review_count = db.query(Review).filter(Review.place_id == place.id).count()
        like_count = db.query(PlaceLike).filter(PlaceLike.place_id == place.id).count()
        
        # Calculate distance if location provided
        distance = None
        if search_request.latitude and search_request.longitude and place.latitude and place.longitude:
            distance = calculate_distance(
                search_request.latitude, search_request.longitude,
                place.latitude, place.longitude
            )
        
        place_dict.update({
            'review_count': review_count,
            'like_count': like_count,
            'distance': distance
        })
        
        result_places.append(PlaceWithStats(**place_dict))
    
    # Sort by distance if location-based search
    if search_request.latitude and search_request.longitude and search_request.sort_by == "distance":
        result_places.sort(key=lambda x: x.distance or float('inf'))
    
    total_pages = math.ceil(total / search_request.page_size)
    
    return PlaceSearchResponse(
        places=result_places,
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


@router.post("/", response_model=PlaceSchema)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    """Create a new place"""
    db_place = Place(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@router.put("/{place_id}", response_model=PlaceSchema)
def update_place(place_id: int, place_update: PlaceUpdate, db: Session = Depends(get_db)):
    """Update a place"""
    db_place = db.query(Place).filter(Place.id == place_id).first()
    
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    update_data = place_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_place, field, value)
    
    db.commit()
    db.refresh(db_place)
    return db_place


@router.delete("/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):
    """Delete a place (soft delete)"""
    db_place = db.query(Place).filter(Place.id == place_id).first()
    
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    db_place.is_active = False
    db.commit()
    
    return {"message": "Place deleted successfully"}


@router.post("/{place_id}/like")
def like_place(place_id: int, user_id: int = Query(..., description="User ID"), db: Session = Depends(get_db)):
    """Like or unlike a place"""
    # Check if place exists
    place = db.query(Place).filter(Place.id == place_id, Place.is_active == True).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    # Check if already liked
    existing_like = db.query(PlaceLike).filter(
        PlaceLike.place_id == place_id,
        PlaceLike.user_id == user_id
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        db.commit()
        return {"message": "Place unliked", "liked": False}
    else:
        # Like
        new_like = PlaceLike(place_id=place_id, user_id=user_id)
        db.add(new_like)
        db.commit()
        return {"message": "Place liked", "liked": True}
