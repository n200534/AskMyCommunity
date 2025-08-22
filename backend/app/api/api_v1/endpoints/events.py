from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from app.core.database import get_collection

router = APIRouter()

class EventBase(BaseModel):
    title: str
    description: str
    date: datetime
    location: str
    category: str
    organizer: str
    contact_info: Optional[str] = None
    website: Optional[str] = None
    tags: List[str] = []

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    category: Optional[str] = None
    organizer: Optional[str] = None
    contact_info: Optional[str] = None
    website: Optional[str] = None
    tags: Optional[List[str]] = None

class Event(EventBase):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    attendees: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Local Food Festival",
                "description": "A celebration of local cuisine and culture",
                "date": "2024-06-15T18:00:00",
                "location": "Downtown Plaza",
                "category": "Food & Culture",
                "organizer": "Local Community Group",
                "tags": ["food", "festival", "local", "culture"]
            }
        }

@router.get("/", response_model=List[Event])
async def list_events(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None
):
    """
    List events with optional filtering.
    """
    try:
        collection = get_collection("events")
        
        # Build filter
        filter_query = {}
        if category:
            filter_query["category"] = {"$regex": category, "$options": "i"}
        if date_from or date_to:
            date_filter = {}
            if date_from:
                date_filter["$gte"] = date_from
            if date_to:
                date_filter["$lte"] = date_to
            filter_query["date"] = date_filter
        if search:
            filter_query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        
        # Get events
        cursor = collection.find(filter_query).sort("date", 1).skip(skip).limit(limit)
        events = await cursor.to_list(length=limit)
        
        return [Event(**event) for event in events]
        
    except Exception as e:
        print(f"Error listing events: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing events"
        )

@router.get("/{event_id}", response_model=Event)
async def get_event(event_id: str):
    """
    Get a specific event by ID.
    """
    try:
        if not ObjectId.is_valid(event_id):
            raise HTTPException(status_code=400, detail="Invalid event ID")
        
        collection = get_collection("events")
        event = await collection.find_one({"_id": ObjectId(event_id)})
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return Event(**event)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving event: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while retrieving event"
        )

@router.post("/", response_model=Event)
async def create_event(event: EventCreate):
    """
    Create a new event.
    """
    try:
        collection = get_collection("events")
        
        # Create event with default values
        event_data = Event(**event.dict())
        result = await collection.insert_one(event_data.dict(by_alias=True))
        
        # Get the created event
        created_event = await collection.find_one({"_id": result.inserted_id})
        return Event(**created_event)
        
    except Exception as e:
        print(f"Error creating event: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while creating event"
        )

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: str, event_update: EventUpdate):
    """
    Update an event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            raise HTTPException(status_code=400, detail="Invalid event ID")
        
        collection = get_collection("events")
        
        # Check if event exists
        existing_event = await collection.find_one({"_id": ObjectId(event_id)})
        if not existing_event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Prepare update data
        update_data = event_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        # Update event
        result = await collection.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Get updated event
        updated_event = await collection.find_one({"_id": ObjectId(event_id)})
        return Event(**updated_event)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating event: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while updating event"
        )

@router.post("/{event_id}/attend")
async def attend_event(event_id: str):
    """
    Mark attendance for an event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            raise HTTPException(status_code=400, detail="Invalid event ID")
        
        collection = get_collection("events")
        
        # Increment attendee count
        result = await collection.update_one(
            {"_id": ObjectId(event_id)},
            {"$inc": {"attendees": 1}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Get updated event
        updated_event = await collection.find_one({"_id": ObjectId(event_id)})
        
        return {
            "message": "Attendance recorded successfully",
            "event_id": event_id,
            "attendees": updated_event["attendees"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error recording attendance: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while recording attendance"
        )

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """
    Delete an event.
    """
    try:
        if not ObjectId.is_valid(event_id):
            raise HTTPException(status_code=400, detail="Invalid event ID")
        
        collection = get_collection("events")
        
        result = await collection.delete_one({"_id": ObjectId(event_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return {"message": "Event deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting event: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while deleting event"
        )

@router.get("/categories/list")
async def list_event_categories():
    """
    Get list of all available event categories.
    """
    try:
        collection = get_collection("events")
        
        # Get distinct categories
        categories = await collection.distinct("category")
        
        return {"categories": sorted(categories)}
        
    except Exception as e:
        print(f"Error listing event categories: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while listing event categories"
        )

@router.get("/upcoming", response_model=List[Event])
async def get_upcoming_events(limit: int = 10):
    """
    Get upcoming events.
    """
    try:
        collection = get_collection("events")
        
        # Get events from now onwards
        now = datetime.utcnow()
        cursor = collection.find({"date": {"$gte": now}}).sort("date", 1).limit(limit)
        events = await cursor.to_list(length=limit)
        
        return [Event(**event) for event in events]
        
    except Exception as e:
        print(f"Error getting upcoming events: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while getting upcoming events"
        )
