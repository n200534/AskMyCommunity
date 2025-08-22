from playwright.async_api import async_playwright
from typing import List, Dict, Any
import asyncio
import re
from datetime import datetime

class GoogleMapsScraper:
    def __init__(self):
        self.base_url = "https://www.google.com/maps"
    
    async def search_places(self, query: str, location: str = None) -> List[Dict[str, Any]]:
        """
        Search for places on Google Maps and extract information.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Construct search URL
                search_query = query
                if location:
                    search_query += f" in {location}"
                
                search_url = f"{self.base_url}/search/{search_query.replace(' ', '+')}"
                await page.goto(search_url)
                
                # Wait for results to load
                await page.wait_for_selector('[data-value="Overview"]', timeout=10000)
                
                # Extract place information
                places = await self._extract_places(page)
                
                await browser.close()
                return places
                
            except Exception as e:
                print(f"Error scraping Google Maps: {e}")
                await browser.close()
                return []
    
    async def _extract_places(self, page) -> List[Dict[str, Any]]:
        """
        Extract place information from the Google Maps page.
        """
        places = []
        
        try:
            # Wait for place cards to load
            await page.wait_for_selector('a[href*="/place/"]', timeout=10000)
            
            # Get all place links
            place_links = await page.query_selector_all('a[href*="/place/"]')
            
            for i, link in enumerate(place_links[:10]):  # Limit to first 10 results
                try:
                    # Get place URL
                    href = await link.get_attribute('href')
                    if not href or '/place/' not in href:
                        continue
                    
                    # Extract place name
                    name_element = await link.query_selector('h3, h4, [role="heading"]')
                    if not name_element:
                        continue
                    
                    name = await name_element.text_content()
                    if not name or len(name.strip()) < 2:
                        continue
                    
                    # Get basic info
                    place_info = {
                        'name': name.strip(),
                        'source': 'google_maps',
                        'source_url': f"https://www.google.com{href}",
                        'scraped_at': datetime.utcnow().isoformat()
                    }
                    
                    # Try to get rating
                    rating_element = await link.query_selector('[aria-label*="stars"], [aria-label*="rating"]')
                    if rating_element:
                        rating_text = await rating_element.get_attribute('aria-label')
                        if rating_text:
                            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                            if rating_match:
                                place_info['rating'] = float(rating_match.group(1))
                    
                    # Try to get category/type
                    category_element = await link.query_selector('[aria-label*="category"], [aria-label*="type"]')
                    if category_element:
                        category = await category_element.text_content()
                        if category:
                            place_info['category'] = category.strip()
                    
                    # Try to get address
                    address_element = await link.query_selector('[aria-label*="address"], [aria-label*="location"]')
                    if address_element:
                        address = await address_element.text_content()
                        if address:
                            place_info['address'] = address.strip()
                    
                    if place_info['name'] and 'category' in place_info:
                        places.append(place_info)
                    
                except Exception as e:
                    print(f"Error extracting place {i}: {e}")
                    continue
            
        except Exception as e:
            print(f"Error extracting places: {e}")
        
        return places
    
    async def get_place_details(self, place_url: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific place.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(place_url)
                await page.wait_for_selector('[data-value="Overview"]', timeout=10000)
                
                # Extract detailed information
                details = await self._extract_place_details(page)
                
                await browser.close()
                return details
                
            except Exception as e:
                print(f"Error getting place details: {e}")
                await browser.close()
                return {}
    
    async def _extract_place_details(self, page) -> Dict[str, Any]:
        """
        Extract detailed information about a place.
        """
        details = {}
        
        try:
            # Get place name
            name_element = await page.query_selector('h1, [role="heading"]')
            if name_element:
                details['name'] = await name_element.text_content()
            
            # Get rating
            rating_element = await page.query_selector('[aria-label*="stars"], [aria-label*="rating"]')
            if rating_element:
                rating_text = await rating_element.get_attribute('aria-label')
                if rating_text:
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        details['rating'] = float(rating_match.group(1))
            
            # Get address
            address_element = await page.query_selector('[aria-label*="address"], [aria-label*="location"]')
            if address_element:
                details['address'] = await address_element.text_content()
            
            # Get phone number
            phone_element = await page.query_selector('[aria-label*="phone"], [aria-label*="call"]')
            if phone_element:
                details['phone'] = await phone_element.text_content()
            
            # Get website
            website_element = await page.query_selector('a[href^="http"]')
            if website_element:
                details['website'] = await website_element.get_attribute('href')
            
            # Get hours
            hours_element = await page.query_selector('[aria-label*="hours"], [aria-label*="open"]')
            if hours_element:
                details['hours'] = await hours_element.text_content()
            
            # Get price level
            price_element = await page.query_selector('[aria-label*="price"], [aria-label*="cost"]')
            if price_element:
                details['price_level'] = await price_element.text_content()
            
        except Exception as e:
            print(f"Error extracting place details: {e}")
        
        return details
