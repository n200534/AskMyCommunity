# AI Integration Guide for AskMyCommunity

## Current AI Implementation

### 1. **Custom Rule-Based AI** (Default)
- **What it does**: Simple keyword matching, scoring, and pattern recognition
- **Pros**: Fast, free, no API costs, works offline
- **Cons**: Limited intelligence, basic recommendations
- **Best for**: MVP, testing, cost-sensitive applications

### 2. **OpenAI Integration** (Recommended)
- **What it does**: Uses GPT-3.5/GPT-4 for intelligent recommendations
- **Pros**: Highly intelligent, understands context, natural language processing
- **Cons**: API costs, requires internet
- **Best for**: Production applications, advanced AI features

### 3. **Google AI Integration** (Alternative)
- **What it does**: Uses Google's Gemini Pro for recommendations
- **Pros**: Competitive with OpenAI, good pricing
- **Cons**: Newer service, less mature ecosystem
- **Best for**: Cost-effective AI, Google ecosystem integration

## Setup Instructions

### 1. Environment Configuration

Add these to your `.env` file:

```env
# AI Services
OPENAI_API_KEY=your-openai-api-key-here
GOOGLE_AI_API_KEY=your-google-ai-api-key-here
AI_SERVICE=openai  # or "google_ai" or "custom"
```

### 2. Get API Keys

#### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up/Login
3. Go to API Keys section
4. Create new secret key
5. Copy the key to your `.env` file

#### Google AI API Key
1. Go to https://makersuite.google.com/
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy the key to your `.env` file

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Usage Examples

#### Using the AI Factory (Recommended)

```python
from app.services.ai_factory import ai_factory

# Generate recommendations
recommendations = await ai_factory.generate_recommendations(
    query="romantic dinner spots",
    available_places=places_data,
    user_preferences={"location": "Bangalore", "price_range": "$$$"},
    limit=5
)

# Extract user intent
intent = await ai_factory.extract_intent("cozy cafe for work")
# Returns: {"place_type": "cafe", "mood": "cozy", "activity_type": "work", ...}
```

#### Direct Service Usage

```python
from app.services.openai_service import openai_service

# OpenAI specific features
recommendations = await openai_service.generate_recommendations(
    query="best coffee shops",
    available_places=places,
    limit=3
)

# Generate place descriptions
description = await openai_service.generate_place_description(place_data)
```

## AI Features Comparison

| Feature | Custom AI | OpenAI | Google AI |
|---------|-----------|--------|-----------|
| **Basic Recommendations** | ✅ | ✅ | ✅ |
| **Intent Extraction** | ✅ | ✅ | ✅ |
| **Natural Language Understanding** | ❌ | ✅ | ✅ |
| **Context Awareness** | ❌ | ✅ | ✅ |
| **Place Description Generation** | ❌ | ✅ | ✅ |
| **Cost** | Free | $0.002/1K tokens | $0.0005/1K tokens |
| **Speed** | Fast | Medium | Medium |
| **Offline** | ✅ | ❌ | ❌ |

## Cost Estimation

### OpenAI Pricing (GPT-3.5-turbo)
- **Input**: $0.0015 per 1K tokens
- **Output**: $0.002 per 1K tokens
- **Estimated cost per recommendation**: ~$0.01-0.05

### Google AI Pricing (Gemini Pro)
- **Input**: $0.0005 per 1K tokens
- **Output**: $0.0015 per 1K tokens
- **Estimated cost per recommendation**: ~$0.005-0.02

## Advanced AI Features

### 1. **Smart Recommendations**
```python
# AI understands complex queries
query = "quiet place for first date with good food and romantic ambiance"
# AI will find places matching all criteria
```

### 2. **Intent Understanding**
```python
# AI extracts detailed intent
intent = await ai_factory.extract_intent("cozy cafe for work meeting")
# Returns: {
#   "place_type": "cafe",
#   "mood": "cozy", 
#   "activity_type": "work",
#   "group_size": "small",
#   "time_specific": false
# }
```

### 3. **Dynamic Place Descriptions**
```python
# AI generates engaging descriptions
description = await openai_service.generate_place_description(place_data)
# Returns: "A charming rooftop cafe with panoramic city views, perfect for..."
```

## Switching Between AI Services

### In Code
```python
# Use specific service
recommendations = await ai_factory.generate_recommendations(
    query="best restaurants",
    available_places=places,
    service_name="openai"  # or "google_ai" or "custom"
)
```

### In Configuration
```env
# Change default service
AI_SERVICE=google_ai
```

## Best Practices

### 1. **Fallback Strategy**
Always implement fallback to custom AI if external services fail:

```python
try:
    recommendations = await openai_service.generate_recommendations(...)
except Exception:
    recommendations = custom_ai_service.generate_recommendations(...)
```

### 2. **Rate Limiting**
Implement rate limiting to control costs:

```python
import asyncio
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(60 / calls_per_minute)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### 3. **Caching**
Cache AI responses to reduce API calls:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_recommendations(query_hash, places_hash):
    return ai_service.generate_recommendations(...)
```

## Monitoring and Analytics

### Track AI Usage
```python
# Log AI service usage
import logging

logger = logging.getLogger(__name__)

async def generate_recommendations_with_logging(...):
    start_time = time.time()
    recommendations = await ai_service.generate_recommendations(...)
    duration = time.time() - start_time
    
    logger.info(f"AI recommendation generated in {duration}s, cost: ${estimated_cost}")
    return recommendations
```

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Check if key is correctly set in `.env`
   - Verify key has proper permissions
   - Check API quota and billing

2. **Rate Limiting**
   - Implement exponential backoff
   - Use multiple API keys if needed
   - Cache responses

3. **High Costs**
   - Implement caching
   - Use cheaper models (GPT-3.5 vs GPT-4)
   - Optimize prompts to reduce token usage

4. **Poor Recommendations**
   - Improve prompt engineering
   - Add more context to queries
   - Fine-tune parameters (temperature, max_tokens)

## Next Steps

1. **Choose your AI service** based on your needs and budget
2. **Set up API keys** and configure environment
3. **Test with sample data** to ensure everything works
4. **Implement monitoring** to track usage and costs
5. **Optimize prompts** for better results
6. **Add caching** to reduce API calls and costs
