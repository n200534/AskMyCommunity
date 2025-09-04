"""
Seed data for development and testing
"""

from sqlalchemy.orm import Session
from ..models.place import Place
from ..models.user import User
from ..core.database import SessionLocal
from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_sample_places():
    """Create sample places for testing"""
    sample_places = [
        {
            "name": "Blue Tokai Coffee",
            "description": "Cozy rooftop cafe with amazing city views and great coffee. Perfect for work or casual meetings.",
            "place_type": "cafe",
            "address": "123 MG Road, Bangalore",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "rating": 4.8,
            "price_range": "$$",
            "phone": "+91-9876543210",
            "website": "https://bluetokaicoffee.com",
            "opening_hours": json.dumps({
                "monday": "7:00 AM - 10:00 PM",
                "tuesday": "7:00 AM - 10:00 PM",
                "wednesday": "7:00 AM - 10:00 PM",
                "thursday": "7:00 AM - 10:00 PM",
                "friday": "7:00 AM - 11:00 PM",
                "saturday": "8:00 AM - 11:00 PM",
                "sunday": "8:00 AM - 10:00 PM"
            }),
            "amenities": json.dumps(["wifi", "outdoor_seating", "pet_friendly", "parking"]),
            "images": json.dumps([
                "https://example.com/blue-tokai-1.jpg",
                "https://example.com/blue-tokai-2.jpg"
            ]),
            "is_verified": True
        },
        {
            "name": "Cubbon Park",
            "description": "Perfect for morning walks and weekend picnics. Beautiful green space in the heart of the city.",
            "place_type": "park",
            "address": "Cubbon Park, Bangalore",
            "latitude": 12.9767,
            "longitude": 77.5928,
            "rating": 4.7,
            "price_range": "Free",
            "opening_hours": json.dumps({
                "monday": "6:00 AM - 6:00 PM",
                "tuesday": "6:00 AM - 6:00 PM",
                "wednesday": "6:00 AM - 6:00 PM",
                "thursday": "6:00 AM - 6:00 PM",
                "friday": "6:00 AM - 6:00 PM",
                "saturday": "6:00 AM - 6:00 PM",
                "sunday": "6:00 AM - 6:00 PM"
            }),
            "amenities": json.dumps(["walking_trails", "playground", "benches", "nature"]),
            "images": json.dumps([
                "https://example.com/cubbon-park-1.jpg",
                "https://example.com/cubbon-park-2.jpg"
            ]),
            "is_verified": True
        },
        {
            "name": "Bangalore Palace",
            "description": "Historic palace with beautiful architecture and gardens. A must-visit for history enthusiasts.",
            "place_type": "tourist_attraction",
            "address": "Palace Road, Bangalore",
            "latitude": 12.9981,
            "longitude": 77.5925,
            "rating": 4.6,
            "price_range": "$$$",
            "phone": "+91-9876543211",
            "opening_hours": json.dumps({
                "monday": "10:00 AM - 5:30 PM",
                "tuesday": "10:00 AM - 5:30 PM",
                "wednesday": "10:00 AM - 5:30 PM",
                "thursday": "10:00 AM - 5:30 PM",
                "friday": "10:00 AM - 5:30 PM",
                "saturday": "10:00 AM - 5:30 PM",
                "sunday": "10:00 AM - 5:30 PM"
            }),
            "amenities": json.dumps(["guided_tours", "photography", "gift_shop", "parking"]),
            "images": json.dumps([
                "https://example.com/palace-1.jpg",
                "https://example.com/palace-2.jpg"
            ]),
            "is_verified": True
        },
        {
            "name": "Toit Brewery",
            "description": "Famous brewery with great food and craft beer. Perfect for evening hangouts with friends.",
            "place_type": "restaurant",
            "address": "Indiranagar, Bangalore",
            "latitude": 12.9716,
            "longitude": 77.6412,
            "rating": 4.5,
            "price_range": "$$$",
            "phone": "+91-9876543212",
            "website": "https://toit.in",
            "opening_hours": json.dumps({
                "monday": "12:00 PM - 11:30 PM",
                "tuesday": "12:00 PM - 11:30 PM",
                "wednesday": "12:00 PM - 11:30 PM",
                "thursday": "12:00 PM - 11:30 PM",
                "friday": "12:00 PM - 12:30 AM",
                "saturday": "12:00 PM - 12:30 AM",
                "sunday": "12:00 PM - 11:30 PM"
            }),
            "amenities": json.dumps(["live_music", "outdoor_seating", "bar", "parking"]),
            "images": json.dumps([
                "https://example.com/toit-1.jpg",
                "https://example.com/toit-2.jpg"
            ]),
            "is_verified": True
        },
        {
            "name": "Lalbagh Botanical Garden",
            "description": "Beautiful botanical garden with diverse plant species. Great for nature lovers and photography.",
            "place_type": "garden",
            "address": "Lalbagh, Bangalore",
            "latitude": 12.9507,
            "longitude": 77.5848,
            "rating": 4.4,
            "price_range": "$$",
            "phone": "+91-9876543213",
            "opening_hours": json.dumps({
                "monday": "6:00 AM - 7:00 PM",
                "tuesday": "6:00 AM - 7:00 PM",
                "wednesday": "6:00 AM - 7:00 PM",
                "thursday": "6:00 AM - 7:00 PM",
                "friday": "6:00 AM - 7:00 PM",
                "saturday": "6:00 AM - 7:00 PM",
                "sunday": "6:00 AM - 7:00 PM"
            }),
            "amenities": json.dumps(["walking_trails", "photography", "nature", "greenhouse"]),
            "images": json.dumps([
                "https://example.com/lalbagh-1.jpg",
                "https://example.com/lalbagh-2.jpg"
            ]),
            "is_verified": True
        },
        {
            "name": "Commercial Street",
            "description": "Famous shopping street with traditional and modern stores. Perfect for street shopping.",
            "place_type": "shopping",
            "address": "Commercial Street, Bangalore",
            "latitude": 12.9767,
            "longitude": 77.6101,
            "rating": 4.2,
            "price_range": "$$",
            "opening_hours": json.dumps({
                "monday": "10:00 AM - 9:00 PM",
                "tuesday": "10:00 AM - 9:00 PM",
                "wednesday": "10:00 AM - 9:00 PM",
                "thursday": "10:00 AM - 9:00 PM",
                "friday": "10:00 AM - 9:00 PM",
                "saturday": "10:00 AM - 9:00 PM",
                "sunday": "10:00 AM - 9:00 PM"
            }),
            "amenities": json.dumps(["shopping", "street_food", "bargaining", "parking"]),
            "images": json.dumps([
                "https://example.com/commercial-1.jpg",
                "https://example.com/commercial-2.jpg"
            ]),
            "is_verified": True
        }
    ]
    
    return sample_places


def create_sample_users():
    """Create sample users for testing"""
    sample_users = [
        {
            "email": "john@example.com",
            "username": "john_doe",
            "full_name": "John Doe",
            "hashed_password": pwd_context.hash("password123"),
            "bio": "Love exploring new places and trying different cuisines",
            "location": "Bangalore, India",
            "is_verified": True
        },
        {
            "email": "jane@example.com",
            "username": "jane_smith",
            "full_name": "Jane Smith",
            "hashed_password": pwd_context.hash("password123"),
            "bio": "Coffee enthusiast and nature lover",
            "location": "Bangalore, India",
            "is_verified": True
        }
    ]
    
    return sample_users


def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Place).count() > 0:
            print("Database already seeded")
            return
        
        # Create sample places
        sample_places = create_sample_places()
        for place_data in sample_places:
            place = Place(**place_data)
            db.add(place)
        
        # Create sample users
        sample_users = create_sample_users()
        for user_data in sample_users:
            user = User(**user_data)
            db.add(user)
        
        db.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
