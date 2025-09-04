from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PlaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    place_type: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    rating: Optional[float] = Field(0.0, ge=0, le=5)
    price_range: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=500)
    opening_hours: Optional[str] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    place_type: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    rating: Optional[float] = Field(None, ge=0, le=5)
    price_range: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=500)
    opening_hours: Optional[str] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None


class Place(PlaceBase):
    id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PlaceWithStats(Place):
    review_count: int = 0
    like_count: int = 0
    distance: Optional[float] = None  # Distance from user location in km


class PlaceSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    place_type: Optional[str] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_price: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    radius: Optional[float] = Field(None, gt=0, le=100)  # Radius in km
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str = Field("relevance", regex="^(relevance|rating|distance|price)$")


class PlaceSearchResponse(BaseModel):
    places: List[PlaceWithStats]
    total: int
    page: int
    page_size: int
    total_pages: int
    query: str
    filters_applied: dict
