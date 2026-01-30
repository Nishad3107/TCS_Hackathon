from langchain_core.output_parsers import PydanticOutputParser
from schemas import ItineraryRequest, TravelItinerary
from models import ModelFactory
from prompts import EXTRACTION_PROMPT, PLANNING_PROMPT
from tools import find_places, check_weather

class TravelAgent:
    def __init__(self):
        self.llm = ModelFactory.get_model()
        self.extractor_parser = PydanticOutputParser(pydantic_object=ItineraryRequest)
        self.planner_parser = PydanticOutputParser(pydantic_object=TravelItinerary)
    
    def understand_request(self, user_input: str) -> ItineraryRequest:
        """
        Phase 1: NLU - Extract structured data.
        """
        format_instructions = self.extractor_parser.get_format_instructions()
        prompt = EXTRACTION_PROMPT.format_messages(user_input=user_input)
        prompt[0].content += f"\n\n{format_instructions}"
        
        try:
            response = self.llm.invoke(prompt)
            return self.extractor_parser.parse(response.content)
        except ValueError as e:
            print(f"Error parsing request - Invalid format: {e}")
            return None
        except Exception as e:
            print(f"Error understanding request: {e}")
            print(f"Please check your API configuration and network connection.")
            return None

    def create_itinerary(self, request: ItineraryRequest) -> TravelItinerary:
        """
        Phase 2 & 3: Search & Plan.
        """
        # 1. Gather Information
        print(f"Agent: Searching for attractions in {request.destination}...")
        search_results = find_places(request.destination, request.interests)
        
        # Handle empty search results
        if not search_results or "No specific attractions found" in search_results:
            print("Warning: Limited attraction data available. Generating generic recommendations...")
            search_results = f"Unable to fetch detailed attraction data for {request.destination}. Please use general knowledge about popular attractions."
        
        print(f"Agent: Checking weather for {request.destination}...")
        weather_info = check_weather(request.destination, request.start_date)
        
        # Handle missing weather data
        if not weather_info or "unavailable" in weather_info.lower():
            print("Warning: Weather data unavailable. Using general seasonal information...")
            weather_info = f"Weather information for {request.destination} is currently unavailable. Please consider typical seasonal conditions."
        
        # 2. Generate Plan
        print("Agent: Generating itinerary...")
        format_instructions = self.planner_parser.get_format_instructions()
        prompt = PLANNING_PROMPT.format_messages(
            request_details=request.model_dump_json(),
            search_results=search_results,
            weather_info=weather_info,
            duration=request.duration_days or 3, # Default to 3 if unknown
            destination=request.destination
        )
        prompt[0].content += f"\n\n{format_instructions}"
        
        try:
            response = self.llm.invoke(prompt)
            return self.planner_parser.parse(response.content)
        except ValueError as e:
            print(f"Error parsing itinerary - Invalid format: {e}")
            print("The AI response did not match the expected format. Please try again.")
            return None
        except Exception as e:
            print(f"Error generating itinerary: {e}")
            print("Please check your API configuration and network connection.")
            return None

if __name__ == "__main__":
    # Test
    pass