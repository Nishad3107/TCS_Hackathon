from typing import List, Optional
from pydantic import BaseModel, Field

class ItineraryRequest(BaseModel):
    """Structured request for a travel itinerary."""
    destination: str = Field(..., description="The main city or country to visit.")
    start_date: Optional[str] = Field(None, description="Start date of the trip (e.g., '2023-10-27').")
    end_date: Optional[str] = Field(None, description="End date of the trip.")
    duration_days: Optional[int] = Field(None, description="Duration of the trip in days if dates are not specific.")
    budget: str = Field("Medium", description="Budget level: Low, Medium, High, or Luxury.")
    interests: List[str] = Field(default_factory=list, description="List of user interests (e.g., History, Food, Hiking).")
    travelers: str = Field("Solo", description="Who is traveling (e.g., Solo, Couple, Family).")

class ItineraryDay(BaseModel):
    """Plan for a single day."""
    day_number: int
    date: Optional[str]
    morning_activity: str
    afternoon_activity: str
    evening_activity: str
    accommodation: Optional[str] = None
    
class TravelItinerary(BaseModel):
    """Final Output Itinerary."""
    title: str
    request: ItineraryRequest
    days: List[ItineraryDay]
    summary: str
    total_estimated_cost: Optional[str] = Field(None, description="Estimated total cost for the trip (e.g., '$1500 - $2000').")
