import google.generativeai as genai
from app.core.config import settings
from typing import List, Dict, Any
import json

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def generate_recommendations(
        self, 
        query: str, 
        places_data: List[Dict[str, Any]], 
        user_location: str = None,
        user_preferences: List[str] = None,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Generate AI-powered recommendations using Gemini.
        """
        
        # Prepare the prompt for Gemini
        prompt = self._build_prompt(query, places_data, user_location, user_preferences, context)
        
        try:
            # Generate response from Gemini
            response = await self._generate_response(prompt)
            
            # Parse and structure the response
            structured_response = self._parse_ai_response(response)
            
            return structured_response
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._fallback_response(query, places_data)
    
    def _build_prompt(
        self, 
        query: str, 
        places_data: List[Dict[str, Any]], 
        user_location: str = None,
        user_preferences: List[str] = None,
        context: str = None
    ) -> str:
        """
        Build a comprehensive prompt for the AI model.
        """
        
        prompt = f"""
        You are a local community expert helping someone find great places to visit. 
        
        User Query: "{query}"
        """
        
        if user_location:
            prompt += f"\nUser Location: {user_location}"
        
        if user_preferences:
            prompt += f"\nUser Preferences: {', '.join(user_preferences)}"
        
        if context:
            prompt += f"\nContext: {context}"
        
        prompt += f"""
        
        Available Places Data:
        {json.dumps(places_data, indent=2)}
        
        Please provide:
        1. A personalized recommendation based on the query and available data
        2. Top 3-5 places that best match the user's needs
        3. Reasoning for each recommendation
        4. Any additional tips or considerations
        
        Format your response as JSON with this structure:
        {{
            "summary": "Brief overview of recommendations",
            "places": [
                {{
                    "name": "Place name",
                    "reasoning": "Why this place is recommended",
                    "category": "Place category",
                    "best_for": "What this place is best for"
                }}
            ],
            "additional_tips": "Any extra advice or considerations"
        }}
        
        Be conversational, helpful, and consider the user's specific query and context.
        """
        
        return prompt
    
    async def _generate_response(self, prompt: str) -> str:
        """
        Generate response from Gemini model.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise e
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the AI response and extract structured data.
        """
        try:
            # Try to extract JSON from the response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
                return json.loads(json_str)
            elif "{" in response and "}" in response:
                # Try to find JSON-like structure
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback: return the raw response
                return {
                    "summary": "AI-generated recommendation",
                    "places": [],
                    "additional_tips": response
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured fallback
            return {
                "summary": "AI-generated recommendation",
                "places": [],
                "additional_tips": response
            }
    
    def _fallback_response(self, query: str, places_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Provide a fallback response if AI generation fails.
        """
        return {
            "summary": f"Here are some places that might interest you based on your query: '{query}'",
            "places": places_data[:3],  # Return first 3 places
            "additional_tips": "These are general recommendations. Consider checking reviews and current hours before visiting."
        }
