from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PlaceBase(BaseModel):
    name: str
    address: str
    category: str
    description: Optional[str] = None
    rating: Optional[float] = None
    price_level: Optional[str] = None
    hours: Optional[dict] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: List[str] = []
    source: str  # "google_maps", "reddit", "local_blog"
    source_url: Optional[str] = None

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    price_level: Optional[str] = None
    hours: Optional[dict] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    coordinates: Optional[dict] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    source_url: Optional[str] = None

class Place(PlaceBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    votes: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "The Local Coffee Shop",
                "address": "123 Main St, City, State",
                "category": "Coffee Shop",
                "description": "A cozy local coffee shop with great atmosphere",
                "rating": 4.5,
                "price_level": "$$",
                "tags": ["coffee", "local", "cozy"],
                "source": "google_maps"
            }
        }
