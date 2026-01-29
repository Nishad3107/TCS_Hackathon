# Travel Itinerary AI Agent - Development Plan

## Phase 1: Setup & Core Structure (Current)
- [x] Create project structure
- [x] Define basic dependencies
- [ ] Setup Virtual Environment

## Phase 2: NLU (Natural Language Understanding)
- [ ] specific Model Selection (e.g., Ollama/Llama3, Gemini Flash)
- [ ] Prompt Engineering: Create prompts to extract entities (Destination, Dates, Budget).
- [ ] Pydantic Models: Define structured output for the itinerary request.

## Phase 3: Tools & Data
- [ ] Implement `search_tool`: Connect to a search API (e.g., Serper, Tavily) or Wikipedia to find places.
- [ ] Implement `weather_tool`: (Optional) Check weather for dates.

## Phase 4: Agent Logic
- [ ] Orchestrator: Combine NLU outputs with Search results.
- [ ] Scheduler: Slot activities into morning/afternoon/evening blocks.

## Phase 5: Interface
- [ ] CLI Interaction Loop.
- [ ] (Future) Streamlit or Web UI.
