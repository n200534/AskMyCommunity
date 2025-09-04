"""
OpenAI Integration for Advanced AI Recommendations
"""

import openai
from typing import List, Dict, Any, Optional
import json
from ..core.config import settings


class OpenAIService:
    """OpenAI-powered AI service for intelligent recommendations"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-3.5-turbo"  # or "gpt-4" for better results
    
    async def generate_recommendations(
        self,
        query: str,
        available_places: List[Dict[str, Any]],
        user_preferences: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered recommendations using OpenAI
        """
        if not available_places:
            return []
        
        # Prepare context for AI
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
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful place recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            return recommendations[:limit]
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_recommendations(query, available_places, limit)
    
    async def extract_intent(self, query: str) -> Dict[str, Any]:
        """
        Extract user intent using OpenAI
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
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at understanding user search intent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_intent_extraction(query)
    
    async def generate_place_description(self, place_data: Dict[str, Any]) -> str:
        """
        Generate an AI-powered description for a place
        """
        prompt = f"""
        Write an engaging, SEO-friendly description for this place:
        
        Name: {place_data.get('name', '')}
        Type: {place_data.get('place_type', '')}
        Current Description: {place_data.get('description', '')}
        Rating: {place_data.get('rating', 0)}
        Price Range: {place_data.get('price_range', '')}
        Amenities: {place_data.get('amenities', [])}
        
        Make it:
        - 2-3 sentences
        - Engaging and descriptive
        - Include key selling points
        - SEO-friendly
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional copywriter specializing in place descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return place_data.get('description', '')
    
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
            Address: {place.get('address', '')}
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
        - Previous Likes: {preferences.get('liked_places', [])}
        """
    
    def _fallback_recommendations(self, query: str, places: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
        """Fallback to simple matching if AI fails"""
        # Simple keyword matching fallback
        query_lower = query.lower()
        scored_places = []
        
        for place in places:
            score = 0.0
            if query_lower in place.get('name', '').lower():
                score += 0.4
            if query_lower in place.get('description', '').lower():
                score += 0.3
            if query_lower in place.get('place_type', '').lower():
                score += 0.2
            score += place.get('rating', 0) * 0.1
            
            scored_places.append((place, score))
        
        scored_places.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for i, (place, score) in enumerate(scored_places[:limit]):
            recommendations.append({
                'place_id': place['id'],
                'confidence_score': min(score, 1.0),
                'reason': f"Matches your search for '{query}'",
                'rank': i + 1
            })
        
        return recommendations
    
    def _fallback_intent_extraction(self, query: str) -> Dict[str, Any]:
        """Fallback intent extraction using simple patterns"""
        query_lower = query.lower()
        
        place_types = ["restaurant", "cafe", "bar", "park", "museum", "shopping"]
        price_ranges = ["$", "$$", "$$$", "$$$$"]
        
        return {
            "place_type": next((pt for pt in place_types if pt in query_lower), None),
            "price_range": next((pr for pr in price_ranges if pr in query_lower), None),
            "activity_type": None,
            "location_specific": any(kw in query_lower for kw in ["near me", "nearby", "close to"]),
            "time_specific": any(kw in query_lower for kw in ["tonight", "today", "weekend"]),
            "mood": None,
            "group_size": None
        }


# Global OpenAI service instance
openai_service = OpenAIService()
