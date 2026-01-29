# Travel Itinerary AI Agent

## Project Overview

This project is an AI-powered CLI agent designed to generate personalized travel itineraries. It uses a Large Language Model (LLM) to understand natural language requests and extracts key travel details (destination, dates, budget, interests). It then leverages search tools to find relevant attractions and generates a day-by-day travel plan.

**Key Technologies:**
*   **Language:** Python
*   **Orchestration:** LangChain
*   **Data Validation:** Pydantic
*   **CLI Interface:** Rich
*   **Search Tool:** DuckDuckGo Search
*   **LLM Support:** Ollama (Local), Google Gemini, OpenAI

## Architecture

The project is structured within the `src/` directory:

*   **`main.py`**: The entry point for the CLI application. Handles user interaction and loop.
*   **`src/agent.py`**: Contains the `TravelAgent` class, which manages the core logic:
    *   **Understanding**: Parses user input into structured data using Pydantic.
    *   **Planning**: Orchestrates the search and itinerary generation process.
*   **`src/tools.py`**: Implements external tools, primarily `DuckDuckGoSearchRun` for finding attractions.
*   **`src/models.py`**: Factory for initializing the LLM (supports Local/Ollama, Google, OpenAI).
*   **`src/schemas.py`**: Pydantic models defining the data structures for requests and itineraries.
*   **`src/prompts.py`**: Stores the system prompts used to guide the LLM.

## Setup & Usage

### Prerequisites
*   Python 3.x
*   (Optional) Ollama installed for local model support.
*   (Optional) API Keys for Google Gemini or OpenAI.

### Installation

1.  **Environment Setup**:
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    Copy the example environment file and configure your keys/settings.
    ```bash
    cp .env.example .env
    ```
    *   Edit `.env` to add `GOOGLE_API_KEY`, `OPENAI_API_KEY`, or set `OLLAMA_BASE_URL` and `MODEL_NAME`.

### Running the Agent

Start the interactive CLI:
```bash
python main.py
```

Follow the on-screen prompts to request a trip plan. 
**Example Input:** "Plan a 3-day trip to Kyoto for a couple who loves history and ramen. Budget is medium."

## Development Conventions

*   **Code Style**: Follows standard Python conventions.
*   **Dependency Management**: Dependencies are tracked in `requirements.txt`.
*   **Prompt Engineering**: All prompts should be centralized in `src/prompts.py` to allow for easy tuning.
*   **Type Safety**: Use Pydantic models (`src/schemas.py`) for data exchange between the LLM and the application to ensure structural integrity.
