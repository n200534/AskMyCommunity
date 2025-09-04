from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    query = Column(String(500), nullable=False)  # The search query that led to this recommendation
    confidence_score = Column(Float, default=0.0)  # AI confidence in this recommendation
    reason = Column(Text)  # Why this place was recommended
    is_clicked = Column(Boolean, default=False)
    is_liked = Column(Boolean, default=False)
    feedback = Column(Text)  # User feedback on the recommendation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    place = relationship("Place", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, user_id={self.user_id}, place_id={self.place_id})>"


class SearchQuery(Base):
    __tablename__ = "search_queries"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(500), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for anonymous searches
    results_count = Column(Integer, default=0)
    search_type = Column(String(50), default="general")  # general, specific, location-based
    filters_applied = Column(Text)  # JSON string of applied filters
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<SearchQuery(id={self.id}, query='{self.query}', results_count={self.results_count})>"
