from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from schemas import ItineraryRequest
from models import ModelFactory
from prompts import EXTRACTION_PROMPT, PLANNING_PROMPT
from tools import find_places

class TravelAgent:
    def __init__(self):
        self.llm = ModelFactory.get_model()
        self.extractor_parser = PydanticOutputParser(pydantic_object=ItineraryRequest)
        self.planner_parser = StrOutputParser()
    
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
        except Exception as e:
            print(f"Error parsing request: {e}")
            return None

    def create_itinerary(self, request: ItineraryRequest) -> str:
        """
        Phase 2 & 3: Search & Plan.
        """
        # 1. Gather Information
        print(f"Agent: Searching for attractions in {request.destination}...")
        search_results = find_places(request.destination, request.interests)
        
        # 2. Generate Plan
        print("Agent: Generating itinerary...")
        prompt = PLANNING_PROMPT.format_messages(
            request_details=request.model_dump_json(),
            search_results=search_results,
            duration=request.duration_days or 3, # Default to 3 if unknown
            destination=request.destination
        )
        
        response = self.llm.invoke(prompt)
        return self.planner_parser.parse(response.content)

if __name__ == "__main__":
    # Test
    pass