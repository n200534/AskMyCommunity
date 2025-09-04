from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RecommendationBase(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    confidence_score: Optional[float] = Field(0.0, ge=0, le=1)
    reason: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    place_id: int


class RecommendationUpdate(BaseModel):
    is_clicked: Optional[bool] = None
    is_liked: Optional[bool] = None
    feedback: Optional[str] = None


class Recommendation(RecommendationBase):
    id: int
    user_id: int
    place_id: int
    is_clicked: bool
    is_liked: bool
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class RecommendationWithPlace(Recommendation):
    place: dict  # Place details will be populated


class SearchQueryCreate(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    search_type: str = Field("general", regex="^(general|specific|location-based)$")
    filters_applied: Optional[dict] = None


class SearchQuery(SearchQueryCreate):
    id: int
    user_id: Optional[int] = None
    results_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True
