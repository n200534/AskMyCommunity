from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random

from ....core.database import get_db
from ....models.recommendation import Recommendation, SearchQuery
from ....models.place import Place
from ....schemas.recommendation import (
    Recommendation as RecommendationSchema,
    RecommendationCreate,
    RecommendationUpdate,
    RecommendationWithPlace,
    SearchQueryCreate,
    SearchQuery as SearchQuerySchema
)

router = APIRouter()


@router.post("/search", response_model=SearchQuerySchema)
def log_search_query(
    search_data: SearchQueryCreate,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Log a search query for analytics"""
    search_query = SearchQuery(
        query=search_data.query,
        user_id=user_id,
        search_type=search_data.search_type,
        filters_applied=search_data.filters_applied
    )
    
    db.add(search_query)
    db.commit()
    db.refresh(search_query)
    
    return search_query


@router.get("/", response_model=List[RecommendationWithPlace])
def get_recommendations(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get recommendations for a user"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).order_by(Recommendation.created_at.desc()).limit(limit).all()
    
    result = []
    for rec in recommendations:
        place = db.query(Place).filter(Place.id == rec.place_id).first()
        if place:
            rec_dict = rec.__dict__.copy()
            rec_dict['place'] = {
                'id': place.id,
                'name': place.name,
                'description': place.description,
                'place_type': place.place_type,
                'rating': place.rating,
                'price_range': place.price_range,
                'address': place.address
            }
            result.append(RecommendationWithPlace(**rec_dict))
    
    return result


@router.post("/", response_model=RecommendationSchema)
def create_recommendation(
    recommendation: RecommendationCreate,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Create a new recommendation"""
    # Check if place exists
    place = db.query(Place).filter(Place.id == recommendation.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    db_recommendation = Recommendation(
        user_id=user_id,
        place_id=recommendation.place_id,
        query=recommendation.query,
        confidence_score=recommendation.confidence_score,
        reason=recommendation.reason
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation


@router.put("/{recommendation_id}", response_model=RecommendationSchema)
def update_recommendation(
    recommendation_id: int,
    recommendation_update: RecommendationUpdate,
    db: Session = Depends(get_db)
):
    """Update a recommendation (feedback, like status, etc.)"""
    db_recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if not db_recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    update_data = recommendation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recommendation, field, value)
    
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation


@router.get("/ai-suggestions", response_model=List[RecommendationWithPlace])
def get_ai_suggestions(
    query: str = Query(..., description="Search query"),
    user_id: Optional[int] = Query(None, description="User ID"),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get AI-powered suggestions based on query"""
    # This is a simplified AI suggestion system
    # In production, you'd integrate with actual AI services
    
    # Search for places matching the query
    search_term = f"%{query.lower()}%"
    places = db.query(Place).filter(
        Place.is_active == True,
        (Place.name.ilike(search_term) |
         Place.description.ilike(search_term) |
         Place.place_type.ilike(search_term))
    ).limit(limit * 2).all()  # Get more to randomize
    
    # Randomize and limit results (simplified AI)
    random.shuffle(places)
    selected_places = places[:limit]
    
    # Create recommendations
    recommendations = []
    for i, place in enumerate(selected_places):
        confidence = 0.8 - (i * 0.1)  # Decreasing confidence
        reason = f"Based on your search for '{query}', this {place.place_type.lower()} matches your interests"
        
        rec_dict = {
            'id': f"ai_{place.id}_{i}",
            'user_id': user_id or 0,
            'place_id': place.id,
            'query': query,
            'confidence_score': confidence,
            'reason': reason,
            'is_clicked': False,
            'is_liked': False,
            'feedback': None,
            'created_at': datetime.utcnow(),
            'updated_at': None,
            'place': {
                'id': place.id,
                'name': place.name,
                'description': place.description,
                'place_type': place.place_type,
                'rating': place.rating,
                'price_range': place.price_range,
                'address': place.address
            }
        }
        
        recommendations.append(RecommendationWithPlace(**rec_dict))
    
    return recommendations
