from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from .place import PyObjectId

class RecommendationBase(BaseModel):
    query: str
    user_location: Optional[str] = None
    user_preferences: Optional[List[str]] = None
    context: Optional[str] = None  # e.g., "Saturday night", "date night", "family outing"

class RecommendationCreate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    places: List[dict] = []  # List of recommended places with reasoning
    ai_response: str  # Full AI response explaining the recommendations
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_feedback: Optional[int] = None  # 1-5 rating from user

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "query": "Where should I hang out on Saturday?",
                "user_location": "Downtown",
                "context": "Saturday night",
                "places": [
                    {
                        "name": "The Local Coffee Shop",
                        "reasoning": "Great atmosphere for casual hangouts",
                        "category": "Coffee Shop"
                    }
                ],
                "ai_response": "Based on your query for Saturday hangout spots..."
            }
        }
