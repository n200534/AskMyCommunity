from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    place_type = Column(String(100), nullable=False, index=True)  # cafe, restaurant, park, etc.
    address = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float, default=0.0)
    price_range = Column(String(10))  # $, $$, $$$, etc.
    phone = Column(String(20))
    website = Column(String(500))
    opening_hours = Column(Text)  # JSON string
    amenities = Column(Text)  # JSON string
    images = Column(Text)  # JSON string of image URLs
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="place", cascade="all, delete-orphan")
    likes = relationship("PlaceLike", back_populates="place", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Place(id={self.id}, name='{self.name}', type='{self.place_type}')>"


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    
    def __repr__(self):
        return f"<Review(id={self.id}, place_id={self.place_id}, rating={self.rating})>"


class PlaceLike(Base):
    __tablename__ = "place_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    place = relationship("Place", back_populates="likes")
    user = relationship("User", back_populates="place_likes")
    
    def __repr__(self):
        return f"<PlaceLike(place_id={self.place_id}, user_id={self.user_id})>"
