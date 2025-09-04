"""
Google AI Integration for Advanced Recommendations
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
from ..core.config import settings


class GoogleAIService:
    """Google AI-powered service for intelligent recommendations"""
    
    def __init__(self):
        genai.configure(api_key=settings.google_ai_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Using Gemini Flash for faster responses
    
    async def generate_recommendations(
        self,
        query: str,
        available_places: List[Dict[str, Any]],
        user_preferences: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered recommendations using Google Gemini
        """
        if not available_places:
            return []
        
        places_context = self._prepare_places_context(available_places)
        user_context = self._prepare_user_context(user_preferences)
        
        prompt = f"""
        You are an AI assistant helping users find the best places in their city.
        
        User Query: "{query}"
        {user_context}
        
        Available Places:
        {places_context}
        
        Based on the user's query and preferences, recommend the top {limit} places.
        For each recommendation, provide:
        1. Place ID
        2. Confidence score (0.0 to 1.0)
        3. Reason for recommendation
        4. Rank (1 to {limit})
        
        Return as JSON array with this structure:
        [
            {{
                "place_id": 1,
                "confidence_score": 0.95,
                "reason": "Perfect match for your coffee search with excellent ratings",
                "rank": 1
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            recommendations = json.loads(response.text)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"Google AI API error: {e}")
            return self._fallback_recommendations(query, available_places, limit)
    
    async def extract_intent(self, query: str) -> Dict[str, Any]:
        """
        Extract user intent using Google Gemini
        """
        prompt = f"""
        Analyze this search query and extract the user's intent: "{query}"
        
        Return JSON with these fields:
        {{
            "place_type": "restaurant/cafe/park/etc or null",
            "price_range": "$/$$/$$$/$$$$ or null",
            "activity_type": "dining/entertainment/shopping/etc or null",
            "location_specific": true/false,
            "time_specific": true/false,
            "mood": "romantic/casual/business/etc or null",
            "group_size": "solo/couple/group/family or null"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
            
        except Exception as e:
            print(f"Google AI API error: {e}")
            return self._fallback_intent_extraction(query)
    
    def _prepare_places_context(self, places: List[Dict[str, Any]]) -> str:
        """Prepare places data for AI context"""
        context = []
        for place in places:
            context.append(f"""
            ID: {place.get('id')}
            Name: {place.get('name')}
            Type: {place.get('place_type')}
            Description: {place.get('description', '')}
            Rating: {place.get('rating', 0)}
            Price: {place.get('price_range', '')}
            """)
        return "\n".join(context)
    
    def _prepare_user_context(self, preferences: Optional[Dict[str, Any]]) -> str:
        """Prepare user preferences for AI context"""
        if not preferences:
            return ""
        
        return f"""
        User Preferences:
        - Location: {preferences.get('location', 'Not specified')}
        - Favorite Types: {preferences.get('favorite_types', [])}
        - Price Range: {preferences.get('price_range', 'Any')}
        """
    
    def _fallback_recommendations(self, query: str, places: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Fallback recommendations"""
        # Simple fallback logic
        return []
    
    def _fallback_intent_extraction(self, query: str) -> Dict[str, Any]:
        """Fallback intent extraction"""
        return {
            "place_type": None,
            "price_range": None,
            "activity_type": None,
            "location_specific": False,
            "time_specific": False,
            "mood": None,
            "group_size": None
        }


# Global Google AI service instance
google_ai_service = GoogleAIService()
