from langchain_core.prompts import ChatPromptTemplate

# Prompt to extract structured info from natural language
EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert travel assistant. Your goal is to extract structured travel details from the user's request.\n" \
               "If specific dates are not mentioned, look for relative dates (e.g., 'next weekend') or duration.\n" \
               "If budget is not specified, assume 'Medium'.\n" \
               "If destination is ambiguous, ask for clarification or pick the most likely one.\n" \
               "For interests, infer them from the text (e.g., 'foodie' -> ['Food', 'Culinary'])."),
    ("user", "{user_input}")
])

# Prompt to generate the itinerary based on structured info AND search results

PLANNING_PROMPT = ChatPromptTemplate.from_messages([

    ("system", "You are a professional travel planner. Create a detailed day-by-day itinerary based on the user's request and the provided search results.\n" \

               "Guidelines:\n" \

               "1. Use the 'Search Results' to recommend real places.\n" \

               "2. Group activities logically by location to minimize travel time.\n" \

               "3. Balance the schedule (Morning, Afternoon, Evening).\n" \

               "4. Suggest specific restaurants or food types if 'Food' is an interest.\n" \

               "5. Consider the 'Weather Info' when planning outdoor vs indoor activities.\n" \

               "6. Estimate the 'total_estimated_cost' for the trip (excluding flights) based on the user's budget level and local prices.\n" \

               "7. Provide the output in the requested JSON format."),

    ("user", "Request Details: {request_details}\n\n" \

             "Search Results for Attractions:\n{search_results}\n\n" \

             "Weather Info:\n{weather_info}\n\n" \

             "Create a {duration}-day itinerary for {destination}.")

])
