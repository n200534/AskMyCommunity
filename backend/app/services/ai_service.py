"""
AI Service for generating intelligent recommendations
This is a placeholder for AI integration - in production, you'd integrate with
services like OpenAI, Google AI, or your own ML models
"""

from typing import List, Dict, Any
import random


class AIService:
    """AI service for generating recommendations and insights"""
    
    def __init__(self):
        self.place_types = [
            "restaurant", "cafe", "bar", "park", "museum", "shopping",
            "entertainment", "fitness", "beauty", "health", "education"
        ]
        
        self.price_ranges = ["$", "$$", "$$$", "$$$$"]
        
        self.recommendation_reasons = [
            "Highly rated by users with similar preferences",
            "Popular choice in your area",
            "Matches your search criteria perfectly",
            "Trending spot with great reviews",
            "Perfect for your activity type",
            "Highly recommended by locals"
        ]
    
    def generate_recommendations(
        self, 
        query: str, 
        user_preferences: Dict[str, Any] = None,
        available_places: List[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered recommendations based on query and user preferences
        """
        if not available_places:
            return []
        
        # Simple keyword matching and scoring
        query_lower = query.lower()
        scored_places = []
        
        for place in available_places:
            score = 0.0
            
            # Name matching
            if query_lower in place.get('name', '').lower():
                score += 0.4
            
            # Description matching
            if query_lower in place.get('description', '').lower():
                score += 0.3
            
            # Type matching
            if query_lower in place.get('place_type', '').lower():
                score += 0.2
            
            # Rating boost
            rating = place.get('rating', 0)
            score += rating * 0.1
            
            # Random factor for variety
            score += random.uniform(0, 0.1)
            
            scored_places.append({
                'place': place,
                'score': score,
                'reason': random.choice(self.recommendation_reasons)
            })
        
        # Sort by score and return top results
        scored_places.sort(key=lambda x: x['score'], reverse=True)
        
        recommendations = []
        for i, item in enumerate(scored_places[:limit]):
            recommendations.append({
                'place_id': item['place']['id'],
                'confidence_score': min(item['score'], 1.0),
                'reason': item['reason'],
                'rank': i + 1
            })
        
        return recommendations
    
    def extract_intent(self, query: str) -> Dict[str, Any]:
        """
        Extract user intent from search query
        """
        query_lower = query.lower()
        
        intent = {
            'place_type': None,
            'price_range': None,
            'activity_type': None,
            'location_specific': False,
            'time_specific': False
        }
        
        # Extract place type
        for place_type in self.place_types:
            if place_type in query_lower:
                intent['place_type'] = place_type
                break
        
        # Extract price range
        for price in self.price_ranges:
            if price in query_lower:
                intent['price_range'] = price
                break
        
        # Check for location specificity
        location_keywords = ['near me', 'nearby', 'close to', 'in my area', 'local']
        if any(keyword in query_lower for keyword in location_keywords):
            intent['location_specific'] = True
        
        # Check for time specificity
        time_keywords = ['tonight', 'today', 'weekend', 'morning', 'evening', 'lunch', 'dinner']
        if any(keyword in query_lower for keyword in time_keywords):
            intent['time_specific'] = True
        
        return intent
    
    def generate_insights(self, places: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate insights from place data
        """
        if not places:
            return {}
        
        total_places = len(places)
        avg_rating = sum(place.get('rating', 0) for place in places) / total_places
        
        # Count by type
        type_counts = {}
        for place in places:
            place_type = place.get('place_type', 'unknown')
            type_counts[place_type] = type_counts.get(place_type, 0) + 1
        
        # Count by price range
        price_counts = {}
        for place in places:
            price_range = place.get('price_range', 'unknown')
            price_counts[price_range] = price_counts.get(price_range, 0) + 1
        
        return {
            'total_places': total_places,
            'average_rating': round(avg_rating, 2),
            'most_common_type': max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None,
            'type_distribution': type_counts,
            'price_distribution': price_counts,
            'top_rated': max(places, key=lambda x: x.get('rating', 0)) if places else None
        }


# Global AI service instance
ai_service = AIService()
