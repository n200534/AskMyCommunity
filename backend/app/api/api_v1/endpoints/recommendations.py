from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.recommendation import RecommendationCreate, Recommendation
from app.services.gemini_service import GeminiService
from app.scrapers.google_maps_scraper import GoogleMapsScraper
from app.scrapers.reddit_scraper import RedditScraper
from app.core.database import get_collection
from datetime import datetime
import asyncio

router = APIRouter()
gemini_service = GeminiService()
google_maps_scraper = GoogleMapsScraper()
reddit_scraper = RedditScraper()

@router.post("/query", response_model=dict)
async def get_recommendations(
    recommendation: RecommendationCreate
):
    """
    Get AI-powered recommendations based on user query.
    """
    try:
        # Scrape data from multiple sources
        places_data = []
        
        # Scrape Google Maps
        try:
            google_places = await google_maps_scraper.search_places(
                recommendation.query, 
                recommendation.user_location
            )
            places_data.extend(google_places)
        except Exception as e:
            print(f"Google Maps scraping failed: {e}")
        
        # Scrape Reddit
        try:
            reddit_places = await reddit_scraper.search_local_recommendations(
                recommendation.query
            )
            places_data.extend(reddit_places)
        except Exception as e:
            print(f"Reddit scraping failed: {e}")
        
        if not places_data:
            raise HTTPException(
                status_code=404, 
                detail="No places found for the given query"
            )
        
        # Generate AI recommendations
        ai_response = await gemini_service.generate_recommendations(
            query=recommendation.query,
            places_data=places_data,
            user_location=recommendation.user_location,
            user_preferences=recommendation.user_preferences,
            context=recommendation.context
        )
        
        # Create recommendation record
        recommendation_data = Recommendation(
            query=recommendation.query,
            user_location=recommendation.user_location,
            user_preferences=recommendation.user_preferences,
            context=recommendation.context,
            places=ai_response.get("places", []),
            ai_response=str(ai_response)
        )
        
        # Save to database
        collection = get_collection("recommendations")
        result = await collection.insert_one(recommendation_data.dict(by_alias=True))
        
        # Return the AI response with recommendation ID
        return {
            "recommendation_id": str(result.inserted_id),
            "query": recommendation.query,
            "summary": ai_response.get("summary", ""),
            "places": ai_response.get("places", []),
            "additional_tips": ai_response.get("additional_tips", ""),
            "sources_used": list(set([place.get("source") for place in places_data if place.get("source")]))
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in recommendations endpoint: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while generating recommendations"
        )

@router.get("/{recommendation_id}", response_model=Recommendation)
async def get_recommendation(recommendation_id: str):
    """
    Get a specific recommendation by ID.
    """
    try:
        from bson import ObjectId
        
        if not ObjectId.is_valid(recommendation_id):
            raise HTTPException(status_code=400, detail="Invalid recommendation ID")
        
        collection = get_collection("recommendations")
        recommendation = await collection.find_one({"_id": ObjectId(recommendation_id)})
        
        if not recommendation:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        
        return Recommendation(**recommendation)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving recommendation: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while retrieving recommendation"
        )

@router.post("/{recommendation_id}/feedback")
async def provide_feedback(recommendation_id: str, rating: int):
    """
    Provide feedback on a recommendation (1-5 rating).
    """
    try:
        from bson import ObjectId
        
        if not ObjectId.is_valid(recommendation_id):
            raise HTTPException(status_code=400, detail="Invalid recommendation ID")
        
        if not 1 <= rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        collection = get_collection("recommendations")
        result = await collection.update_one(
            {"_id": ObjectId(recommendation_id)},
            {
                "$set": {
                    "user_feedback": rating,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        
        return {"message": "Feedback recorded successfully", "rating": rating}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error recording feedback: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while recording feedback"
        )

@router.get("/", response_model=List[Recommendation])
async def list_recommendations(
    skip: int = 0,
    limit: int = 10,
    query: Optional[str] = None
):
    """
    List recent recommendations with optional filtering.
    """
    try:
        collection = get_collection("recommendations")
        
        # Build filter
        filter_query = {}
        if query:
            filter_query["query"] = {"$regex": query, "$options": "i"}
        
        # Get recommendations
        cursor = collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
        recommendations = await cursor.to_list(length=limit)
        
        return [Recommendation(**rec) for rec in recommendations]
        
    except Exception as e:
        print(f"Error listing recommendations: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing recommendations"
        )
