"""
Image service for fetching travel destination photos
"""
import requests
import logging

logger = logging.getLogger(__name__)

# Unsplash API (Free - no key needed for basic use)
UNSPLASH_API_URL = "https://source.unsplash.com/800x600/?{query}"

def get_location_image_url(location: str, query_type: str = "travel") -> str:
    """
    Get image URL for a location using Unsplash Source API
    
    Args:
        location: Location name (e.g., "Paris", "Tokyo Tower")
        query_type: Additional search term (e.g., "travel", "landmark", "nature")
    
    Returns:
        Image URL from Unsplash
    """
    try:
        # Clean and improve search query for better matches
        # Remove common words that dilute search
        stop_words = ['the', 'a', 'an', 'and', 'or', 'to', 'in', 'at', 'for']
        location_words = [w for w in location.lower().split() if w not in stop_words]
        clean_location = ' '.join(location_words)
        
        # Build specific search query
        search_query = f"{clean_location} {query_type}".replace(" ", "+")
        
        # Use smaller image size (400x300)
        image_url = f"https://source.unsplash.com/400x300/?{search_query}"
        
        return image_url
    except Exception as e:
        logger.error(f"Error fetching image for {location}: {e}")
        # Return placeholder image
        return "https://source.unsplash.com/400x300/?travel,destination"


def get_destination_hero_image(destination: str) -> str:
    """Get a hero image for the destination"""
    return get_location_image_url(destination, "city,travel")


def get_activity_image(activity_text: str, destination: str) -> str:
    """
    Extract location from activity and get relevant image
    
    Args:
        activity_text: Activity description
        destination: Main destination name
    
    Returns:
        Image URL
    """
    # Improved extraction: look for proper nouns and landmarks
    import re
    
    # First, try to find specific landmarks or place names (capitalized phrases)
    # Look for patterns like "Temple", "Palace", "Museum", "Square", etc.
    landmark_keywords = ['temple', 'palace', 'museum', 'square', 'stupa', 'monastery', 
                         'fort', 'castle', 'church', 'cathedral', 'tower', 'garden',
                         'market', 'bazaar', 'valley', 'park', 'lake', 'mountain']
    
    activity_lower = activity_text.lower()
    
    # Try to find landmark keywords
    for keyword in landmark_keywords:
        if keyword in activity_lower:
            # Get words around the keyword
            pattern = r'(\w+\s+){0,2}' + keyword + r'(\s+\w+){0,2}'
            match = re.search(pattern, activity_text, re.IGNORECASE)
            if match:
                place = match.group(0).strip()
                return get_location_image_url(f"{place} {destination}", "landmark")
    
    # Fallback: Extract capitalized words (likely place names)
    words = activity_text.split()
    potential_places = [word.strip('.,!?()') for word in words if word and len(word) > 3 and word[0].isupper()]
    
    if potential_places and len(potential_places) >= 2:
        # Use first two capitalized words (likely a place name)
        place = ' '.join(potential_places[:2])
        return get_location_image_url(f"{place} {destination}", "landmark")
    elif potential_places:
        place = potential_places[0]
        return get_location_image_url(f"{place} {destination}", "travel")
    else:
        # Ultimate fallback to destination
        return get_location_image_url(destination, "city")


def get_fallback_image() -> str:
    """Get a generic travel image as fallback"""
    return "https://source.unsplash.com/800x600/?travel,vacation"
