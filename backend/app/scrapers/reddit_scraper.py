import praw
from typing import List, Dict, Any
from app.core.config import settings
import re
from datetime import datetime

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )
    
    async def search_local_recommendations(self, query: str, subreddit: str = None) -> List[Dict[str, Any]]:
        """
        Search Reddit for local recommendations and discussions.
        """
        try:
            places = []
            
            # Default subreddits for local recommendations
            if not subreddit:
                subreddits = [
                    "local", "cityname", "food", "restaurants", 
                    "coffee", "bars", "nightlife", "activities"
                ]
            else:
                subreddits = [subreddit]
            
            for sub in subreddits:
                try:
                    subreddit_instance = self.reddit.subreddit(sub)
                    
                    # Search for posts related to the query
                    search_results = subreddit_instance.search(
                        query, 
                        sort='relevance', 
                        time_filter='year',
                        limit=20
                    )
                    
                    for post in search_results:
                        place_info = self._extract_place_from_post(post, query)
                        if place_info:
                            places.append(place_info)
                            
                except Exception as e:
                    print(f"Error searching subreddit {sub}: {e}")
                    continue
            
            return places
            
        except Exception as e:
            print(f"Error in Reddit scraper: {e}")
            return []
    
    def _extract_place_from_post(self, post, query: str) -> Dict[str, Any]:
        """
        Extract place information from a Reddit post.
        """
        try:
            # Check if post contains relevant information
            if not self._is_relevant_post(post, query):
                return None
            
            # Extract place name from title or content
            place_name = self._extract_place_name(post.title, post.selftext)
            if not place_name:
                return None
            
            # Determine category based on content
            category = self._determine_category(post.title, post.selftext)
            
            # Extract address if available
            address = self._extract_address(post.selftext)
            
            # Extract rating if mentioned
            rating = self._extract_rating(post.selftext)
            
            # Extract tags/keywords
            tags = self._extract_tags(post.title, post.selftext)
            
            place_info = {
                'name': place_name,
                'category': category,
                'source': 'reddit',
                'source_url': f"https://reddit.com{post.permalink}",
                'description': post.selftext[:500] if post.selftext else None,
                'votes': post.score,
                'comments_count': post.num_comments,
                'created_at': datetime.fromtimestamp(post.created_utc).isoformat(),
                'scraped_at': datetime.utcnow().isoformat()
            }
            
            if address:
                place_info['address'] = address
            
            if rating:
                place_info['rating'] = rating
            
            if tags:
                place_info['tags'] = tags
            
            return place_info
            
        except Exception as e:
            print(f"Error extracting place from post: {e}")
            return None
    
    def _is_relevant_post(self, post, query: str) -> bool:
        """
        Check if a post is relevant to the search query.
        """
        query_terms = query.lower().split()
        title_lower = post.title.lower()
        content_lower = post.selftext.lower() if post.selftext else ""
        
        # Check if query terms appear in title or content
        for term in query_terms:
            if term in title_lower or term in content_lower:
                return True
        
        # Check for recommendation keywords
        recommendation_keywords = [
            'recommend', 'suggestion', 'best', 'favorite', 'go to',
            'visit', 'check out', 'try', 'love', 'amazing'
        ]
        
        for keyword in recommendation_keywords:
            if keyword in title_lower or keyword in content_lower:
                return True
        
        return False
    
    def _extract_place_name(self, title: str, content: str) -> str:
        """
        Extract place name from post title or content.
        """
        # Look for patterns like "Restaurant Name" or "Restaurant Name - Description"
        title_patterns = [
            r'^([A-Z][a-zA-Z\s&\'-]+?)(?:\s*[-–—]\s*|\s*:|\s*$)',
            r'^([A-Z][a-zA-Z\s&\'-]+?)(?:\s+in\s+|\s+near\s+)',
            r'([A-Z][a-zA-Z\s&\'-]+?)(?:\s+restaurant|\s+cafe|\s+bar|\s+shop)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, title)
            if match:
                name = match.group(1).strip()
                if len(name) > 2 and len(name) < 100:
                    return name
        
        # If no pattern matches, try to extract from content
        if content:
            # Look for capitalized words that might be place names
            words = content.split()
            potential_names = []
            
            for i, word in enumerate(words):
                if word[0].isupper() and len(word) > 2:
                    # Check if next few words are also capitalized
                    name_parts = [word]
                    for j in range(1, 4):
                        if i + j < len(words) and words[i + j][0].isupper():
                            name_parts.append(words[i + j])
                        else:
                            break
                    
                    if len(name_parts) > 0:
                        potential_names.append(' '.join(name_parts))
            
            # Return the longest potential name
            if potential_names:
                return max(potential_names, key=len)
        
        return None
    
    def _determine_category(self, title: str, content: str) -> str:
        """
        Determine the category of a place based on content.
        """
        text = f"{title} {content}".lower()
        
        categories = {
            'restaurant': ['restaurant', 'food', 'dining', 'eat', 'meal'],
            'cafe': ['cafe', 'coffee', 'tea', 'bakery', 'pastry'],
            'bar': ['bar', 'pub', 'tavern', 'brewery', 'cocktail'],
            'shop': ['shop', 'store', 'market', 'boutique', 'retail'],
            'entertainment': ['theater', 'cinema', 'museum', 'gallery', 'concert'],
            'outdoor': ['park', 'trail', 'beach', 'hiking', 'outdoor'],
            'fitness': ['gym', 'fitness', 'yoga', 'sports', 'workout']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in text:
                    return category
        
        return 'local_place'
    
    def _extract_address(self, content: str) -> str:
        """
        Extract address from post content.
        """
        if not content:
            return None
        
        # Look for address patterns
        address_patterns = [
            r'\d+\s+[A-Z][a-zA-Z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)',
            r'\d+\s+[A-Z][a-zA-Z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)[,\s]+[A-Z][a-zA-Z\s]+(?:,\s*[A-Z]{2}\s*\d{5})?',
        ]
        
        for pattern in address_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(0).strip()
        
        return None
    
    def _extract_rating(self, content: str) -> float:
        """
        Extract rating from post content.
        """
        if not content:
            return None
        
        # Look for rating patterns like "5/5", "4.5 stars", etc.
        rating_patterns = [
            r'(\d+(?:\.\d+)?)\s*/\s*5',
            r'(\d+(?:\.\d+)?)\s*stars?',
            r'(\d+(?:\.\d+)?)\s*out\s*of\s*5'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, content)
            if match:
                rating = float(match.group(1))
                if 0 <= rating <= 5:
                    return rating
        
        return None
    
    def _extract_tags(self, title: str, content: str) -> List[str]:
        """
        Extract relevant tags/keywords from post.
        """
        text = f"{title} {content}".lower()
        
        # Common tags for local places
        common_tags = [
            'local', 'authentic', 'hidden gem', 'popular', 'trendy',
            'family-friendly', 'romantic', 'casual', 'upscale', 'budget-friendly',
            'quick', 'slow', 'quiet', 'lively', 'cozy', 'spacious'
        ]
        
        tags = []
        for tag in common_tags:
            if tag in text:
                tags.append(tag)
        
        return tags
