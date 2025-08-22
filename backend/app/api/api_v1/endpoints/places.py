from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.place import Place, PlaceCreate, PlaceUpdate
from app.core.database import get_collection
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[Place])
async def list_places(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None
):
    """
    List places with optional filtering and search.
    """
    try:
        collection = get_collection("places")
        
        # Build filter
        filter_query = {}
        if category:
            filter_query["category"] = {"$regex": category, "$options": "i"}
        if source:
            filter_query["source"] = source
        if search:
            filter_query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        
        # Get places
        cursor = collection.find(filter_query).sort("votes", -1).skip(skip).limit(limit)
        places = await cursor.to_list(length=limit)
        
        return [Place(**place) for place in places]
        
    except Exception as e:
        print(f"Error listing places: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing places"
        )

@router.get("/{place_id}", response_model=Place)
async def get_place(place_id: str):
    """
    Get a specific place by ID.
    """
    try:
        if not ObjectId.is_valid(place_id):
            raise HTTPException(status_code=400, detail="Invalid place ID")
        
        collection = get_collection("places")
        place = await collection.find_one({"_id": ObjectId(place_id)})
        
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        
        return Place(**place)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving place: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while retrieving place"
        )

@router.post("/", response_model=Place)
async def create_place(place: PlaceCreate):
    """
    Create a new place.
    """
    try:
        collection = get_collection("places")
        
        # Check if place already exists
        existing_place = await collection.find_one({
            "name": place.name,
            "address": place.address
        })
        
        if existing_place:
            raise HTTPException(
                status_code=400, 
                detail="Place with this name and address already exists"
            )
        
        # Create place with default values
        place_data = Place(**place.dict())
        result = await collection.insert_one(place_data.dict(by_alias=True))
        
        # Get the created place
        created_place = await collection.find_one({"_id": result.inserted_id})
        return Place(**created_place)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating place: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while creating place"
        )

@router.put("/{place_id}", response_model=Place)
async def update_place(place_id: str, place_update: PlaceUpdate):
    """
    Update a place.
    """
    try:
        if not ObjectId.is_valid(place_id):
            raise HTTPException(status_code=400, detail="Invalid place ID")
        
        collection = get_collection("places")
        
        # Check if place exists
        existing_place = await collection.find_one({"_id": ObjectId(place_id)})
        if not existing_place:
            raise HTTPException(status_code=404, detail="Place not found")
        
        # Prepare update data
        update_data = place_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update place
        result = await collection.update_one(
            {"_id": ObjectId(place_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Place not found")
        
        # Get updated place
        updated_place = await collection.find_one({"_id": ObjectId(place_id)})
        return Place(**updated_place)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating place: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while updating place"
        )

@router.post("/{place_id}/vote")
async def vote_place(place_id: str, vote: int):
    """
    Vote on a place (positive or negative vote).
    """
    try:
        if not ObjectId.is_valid(place_id):
            raise HTTPException(status_code=400, detail="Invalid place ID")
        
        if vote not in [-1, 1]:
            raise HTTPException(status_code=400, detail="Vote must be -1 (downvote) or 1 (upvote)")
        
        collection = get_collection("places")
        
        # Update vote count
        result = await collection.update_one(
            {"_id": ObjectId(place_id)},
            {"$inc": {"votes": vote}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Place not found")
        
        # Get updated place
        updated_place = await collection.find_one({"_id": ObjectId(place_id)})
        
        return {
            "message": "Vote recorded successfully",
            "place_id": place_id,
            "new_vote_count": updated_place["votes"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error recording vote: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while recording vote"
        )

@router.delete("/{place_id}")
async def delete_place(place_id: str):
    """
    Delete a place.
    """
    try:
        if not ObjectId.is_valid(place_id):
            raise HTTPException(status_code=400, detail="Invalid place ID")
        
        collection = get_collection("places")
        
        result = await collection.delete_one({"_id": ObjectId(place_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Place not found")
        
        return {"message": "Place deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting place: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while deleting place"
        )

@router.get("/categories/list")
async def list_categories():
    """
    Get list of all available place categories.
    """
    try:
        collection = get_collection("places")
        
        # Get distinct categories
        categories = await collection.distinct("category")
        
        return {"categories": sorted(categories)}
        
    except Exception as e:
        print(f"Error listing categories: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing categories"
        )

@router.get("/sources/list")
async def list_sources():
    """
    Get list of all available data sources.
    """
    try:
        collection = get_collection("places")
        
        # Get distinct sources
        sources = await collection.distinct("source")
        
        return {"sources": sorted(sources)}
        
    except Exception as e:
        print(f"Error listing sources: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing sources"
        )
