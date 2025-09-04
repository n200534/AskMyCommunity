"""
AI Service Factory - Unified interface for different AI providers
"""

from typing import List, Dict, Any, Optional
from .ai_service import AIService
from .openai_service import OpenAIService
from .google_ai_service import GoogleAIService
from ..core.config import settings


class AIFactory:
    """Factory class to manage different AI services"""
    
    def __init__(self):
        self.services = {
            "custom": AIService(),
            "openai": OpenAIService(),
            "google_ai": GoogleAIService()
        }
        self.current_service = settings.ai_service
    
    def get_service(self, service_name: Optional[str] = None):
        """Get AI service instance"""
        service_name = service_name or self.current_service
        return self.services.get(service_name, self.services["custom"])
    
    async def generate_recommendations(
        self,
        query: str,
        available_places: List[Dict[str, Any]],
        user_preferences: Optional[Dict[str, Any]] = None,
        limit: int = 5,
        service_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate recommendations using specified AI service"""
        service = self.get_service(service_name)
        
        if hasattr(service, 'generate_recommendations'):
            return await service.generate_recommendations(
                query, available_places, user_preferences, limit
            )
        else:
            # Fallback for sync services
            return service.generate_recommendations(
                query, available_places, user_preferences, limit
            )
    
    async def extract_intent(
        self,
        query: str,
        service_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Extract user intent using specified AI service"""
        service = self.get_service(service_name)
        
        if hasattr(service, 'extract_intent'):
            return await service.extract_intent(query)
        else:
            # Fallback for sync services
            return service.extract_intent(query)
    
    def generate_insights(
        self,
        places: List[Dict[str, Any]],
        service_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate insights using specified AI service"""
        service = self.get_service(service_name)
        return service.generate_insights(places)


# Global AI factory instance
ai_factory = AIFactory()
