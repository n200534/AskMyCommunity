import { GoogleGenerativeAI, GenerativeModel } from '@google/generative-ai';

// Gemini AI client will be initialized in the class

// Import Place type from maps
interface Place {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  rating: number;
  price_level: number;
  place_type: string;
  photo_url?: string;
  phone?: string;
  website?: string;
  opening_hours?: string[];
  description?: string;
  source: string;
  distance?: number;
}

export interface AIRecommendation {
  confidence: number;
  reasoning: string;
  personalized_notes: string;
  best_for: string[];
  avoid_if: string[];
  best_time_to_visit: string;
  local_tips: string[];
}

export interface EnhancedPlace {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  rating: number;
  price_level: number;
  place_type: string;
  photo_url?: string;
  phone?: string;
  website?: string;
  opening_hours?: string[];
  description?: string;
  source: string;
  ai_recommendation?: AIRecommendation;
  ai_confidence?: number;
  ai_rank?: number;
}

// AI service for enhancing scraped place data
export class AIService {
  private static instance: AIService;
  private genAI?: GoogleGenerativeAI;
  private model?: GenerativeModel;

  constructor() {
    if (process.env.GOOGLE_AI_API_KEY) {
      this.genAI = new GoogleGenerativeAI(process.env.GOOGLE_AI_API_KEY);
      this.model = this.genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    }
  }

  static getInstance(): AIService {
    if (!AIService.instance) {
      AIService.instance = new AIService();
    }
    return AIService.instance;
  }

  // Enhance a single place with AI recommendations
  async enhancePlace(place: Record<string, unknown> | Place, userQuery: string): Promise<EnhancedPlace> {
    try {
      if (!process.env.GOOGLE_AI_API_KEY) {
        console.log('Google AI API key not found, returning place without AI enhancement');
        return {
          ...place,
          ai_confidence: 0,
          ai_rank: 0
        } as EnhancedPlace;
      }

      const prompt = this.createEnhancementPrompt(place, userQuery);
      
      if (!this.model) {
        throw new Error('Gemini model not initialized');
      }

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const aiResponse = response.text();
      const aiRecommendation = this.parseAIResponse(aiResponse || '');

      return {
        ...place,
        ai_recommendation: aiRecommendation,
        ai_confidence: aiRecommendation.confidence,
        ai_rank: this.calculateAIRank(aiRecommendation)
      } as EnhancedPlace;

    } catch (error) {
      console.error('AI enhancement error:', error);
      return {
        ...place,
        ai_confidence: 0,
        ai_rank: 0
      } as EnhancedPlace;
    }
  }

  // Enhance multiple places with AI
  async enhancePlaces(places: Place[], userQuery: string): Promise<EnhancedPlace[]> {
    const enhancedPlaces = await Promise.all(
      places.map(place => this.enhancePlace(place, userQuery))
    );

    // Sort by AI rank (highest first)
    return enhancedPlaces.sort((a, b) => (b.ai_rank || 0) - (a.ai_rank || 0));
  }

  // Generate personalized search suggestions
  async generateSearchSuggestions(query: string): Promise<string[]> {
    try {
      if (!process.env.GOOGLE_AI_API_KEY) {
        return this.getDefaultSuggestions(query);
      }

      if (!this.model) {
        throw new Error('Gemini model not initialized');
      }

      const prompt = `You are a travel search assistant. Generate 5 related search suggestions based on the user's query. Make them specific and actionable.

Based on this search query: "${query}", suggest 5 related searches that would help the user find what they're looking for.

Format your response as a simple list, one suggestion per line.`;

      const result = await this.model.generateContent(prompt);
      const response = await result.response;
      const suggestions = response.text();
      return this.parseSuggestions(suggestions || '');

    } catch (error) {
      console.error('AI suggestions error:', error);
      return this.getDefaultSuggestions(query);
    }
  }

  // Create prompt for place enhancement
  private createEnhancementPrompt(place: Place | Record<string, unknown>, userQuery: string): string {
    return `You are a travel expert AI that provides personalized recommendations for places. Analyze the given place information and provide detailed insights, confidence scores, and personalized recommendations.

Place: ${place.name}
Description: ${place.description || place.address}
Type: ${place.place_type}
Rating: ${place.rating}/5
Price Level: ${place.price_level}/3
Source: ${place.source}

User Query: "${userQuery}"

Please provide a JSON response with the following structure:
{
  "confidence": 85,
  "reasoning": "This place matches your search criteria because...",
  "personalized_notes": "Specific insights about this place...",
  "best_for": ["romantic dinner", "special occasions", "fine dining"],
  "avoid_if": ["on a budget", "looking for casual dining"],
  "best_time_to_visit": "7-9 PM for sunset views",
  "local_tips": ["Book 2 months in advance", "Try the tasting menu", "Ask for window seating"]
}

Make sure the response is valid JSON and all fields are present.`;
  }

  // Parse AI response into structured data
  private parseAIResponse(response: string): AIRecommendation {
    try {
      // Try to extract JSON from the response
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return {
          confidence: parsed.confidence || 75,
          reasoning: parsed.reasoning || 'AI analysis available',
          personalized_notes: parsed.personalized_notes || 'Personalized insights provided',
          best_for: parsed.best_for || ['General visit'],
          avoid_if: parsed.avoid_if || ['No specific concerns'],
          best_time_to_visit: parsed.best_time_to_visit || 'Anytime',
          local_tips: parsed.local_tips || ['Check current hours']
        };
      }
    } catch (error) {
      console.error('Error parsing AI response:', error);
    }

    // Fallback response
    return {
      confidence: 70,
      reasoning: 'AI analysis provided based on available information',
      personalized_notes: 'This place matches your search criteria',
      best_for: ['General visit', 'Local experience'],
      avoid_if: ['No specific concerns'],
      best_time_to_visit: 'Anytime',
      local_tips: ['Check current hours', 'Consider making reservations']
    };
  }

  // Calculate AI rank based on recommendation
  private calculateAIRank(recommendation: AIRecommendation): number {
    const confidenceWeight = 0.4;
    const reasoningWeight = 0.3;
    const tipsWeight = 0.3;

    const confidenceScore = recommendation.confidence / 100;
    const reasoningScore = Math.min(recommendation.reasoning.length / 100, 1);
    const tipsScore = Math.min(recommendation.local_tips.length / 5, 1);

    return Math.round(
      (confidenceScore * confidenceWeight + 
       reasoningScore * reasoningWeight + 
       tipsScore * tipsWeight) * 100
    );
  }

  // Parse suggestions from AI response
  private parseSuggestions(response: string): string[] {
    const lines = response.split('\n').filter(line => line.trim());
    return lines.slice(0, 5).map(line => line.replace(/^\d+\.\s*/, '').trim());
  }

  // Default suggestions when AI is not available
  private getDefaultSuggestions(query: string): string[] {
    const baseSuggestions = [
      `${query} near me`,
      `Best ${query} in the area`,
      `${query} with good reviews`,
      `Affordable ${query}`,
      `${query} open now`
    ];
    return baseSuggestions;
  }
}

// Export singleton instance
export const aiService = AIService.getInstance();
