# 🌍 Travel Itinerary AI Agent

An intelligent AI-powered CLI application that generates personalized travel itineraries based on natural language requests. Simply describe your dream trip, and let the AI plan it for you!

## ✨ Features

- 🤖 **Natural Language Understanding**: Describe your trip in plain English
- 🔍 **Smart Search Integration**: Automatically finds top attractions and activities
- 🌤️ **Weather-Aware Planning**: Considers weather conditions for your travel dates
- 📅 **Day-by-Day Itineraries**: Structured morning/afternoon/evening activities
- 💰 **Budget Estimation**: Estimates total trip costs based on your budget level
- ✅ **Activity Validation**: Optional verification that suggested places actually exist
- 📄 **Export Options**: Save itineraries as Markdown or PDF files
- 🌐 **Beautiful Web Interface**: Modern Streamlit app with animations and gradients ✨ **NEW!**
- 🎨 **Elegant CLI**: Rich terminal interface with colors and formatting
- 🔄 **Robust Error Handling**: Graceful handling of API failures and network issues

## 🏗️ Architecture

```
├── app.py                    # 🌐 Streamlit Web Application (NEW!)
├── main.py                   # 💻 CLI Application
├── src/
│   ├── agent.py              # Core TravelAgent class (NLU + Planning)
│   ├── tools.py              # Search and validation tools
│   ├── models.py             # LLM factory (Ollama, Gemini, OpenAI)
│   ├── schemas.py            # Pydantic data models
│   ├── prompts.py            # LLM prompts for extraction and planning
│   ├── validation.py         # Activity validation module
│   └── utils/
│       └── formatting.py     # Markdown and PDF export utilities
├── assets/
│   ├── styles/
│   │   └── custom.css        # Custom CSS with animations
│   └── images/               # Image assets
└── output/                   # Generated itineraries
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- (Optional) [Ollama](https://ollama.ai) for local models
- (Optional) API keys for Google Gemini or OpenAI

### Installation

1. **Clone or download the project**

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your configuration:
   ```env
   # For Google Gemini
   GOOGLE_API_KEY=your_google_api_key_here
   MODEL_NAME=gemini-1.5-flash
   
   # OR for OpenAI
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-4o-mini
   
   # OR for Local Ollama
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=llama3
   ```

### Running the Application

**Option 1: Web Interface (Recommended)** 🌐
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

**Option 2: Command Line Interface** 💻
```bash
python main.py
```

## 💬 Example Usage

### Web Interface
1. Open `http://localhost:8501` in your browser
2. Fill in the beautiful form:
   - 🗺️ Destination: Tokyo
   - 📅 Duration: 5 days
   - 💰 Budget: Medium
   - 🎨 Interests: Food, Culture
   - 👥 Travelers: Couple
3. Click "🚀 Generate Itinerary"
4. Watch the magic happen with animated progress bars!
5. Get your beautiful itinerary with day-by-day cards
6. Optionally validate activities
7. Download as PDF or Markdown

### CLI Interface
```
Where would you like to go? Plan a 5-day trip to Tokyo for a couple who loves food and culture. Budget is medium.

Plan Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Destination: Tokyo
Duration: 5 days
Budget: Medium
Interests: Food, Culture

Proceed with this plan? [y/n] y

Researching & Planning... ⏳

# Your Amazing Tokyo Adventure

**Destination:** Tokyo
**Duration:** 5 days
...
```

## 📋 Supported LLM Providers

| Provider | Models | Setup |
|----------|--------|-------|
| **Ollama** (Local) | llama3, mistral, gemma, etc. | Install Ollama, set `OLLAMA_BASE_URL` |
| **Google Gemini** | gemini-1.5-flash, gemini-1.5-pro | Set `GOOGLE_API_KEY` |
| **OpenAI** | gpt-4o-mini, gpt-4o, gpt-3.5-turbo | Set `OPENAI_API_KEY` |

## 🛠️ Features in Detail

### Natural Language Understanding
The agent uses advanced LLMs to extract structured information from your natural language input:
- Destination
- Travel dates or duration
- Budget level (Low, Medium, High, Luxury)
- Interests and preferences
- Traveler type (Solo, Couple, Family, etc.)

### Smart Planning
- Searches for real attractions using DuckDuckGo
- Checks weather conditions for your dates
- Creates balanced daily schedules
- Groups activities by location to minimize travel time
- Suggests accommodations and dining options

### Activity Validation (NEW!)
Optionally verify that suggested places and attractions actually exist:
```
Validate activities (verify places exist)? [y/n] y
Validating activities... ✓

✅ Verified Places:
- Senso-ji Temple
- Tokyo Skytree

⚠️ Warnings:
- Could not verify 'XYZ Restaurant' - please double-check this location
```

### Export Options
Save your itinerary for offline use:
- **Markdown (.md)**: Perfect for viewing in text editors or GitHub
- **PDF**: Print-ready format for your trip

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MODEL_NAME` | LLM model to use | Yes |
| `GOOGLE_API_KEY` | Google Gemini API key | For Gemini |
| `OPENAI_API_KEY` | OpenAI API key | For OpenAI |
| `OLLAMA_BASE_URL` | Ollama server URL | For Ollama (default: http://localhost:11434) |

## 🚨 Error Handling

The application includes comprehensive error handling:
- ✅ Network connectivity issues
- ✅ API rate limits
- ✅ Empty search results
- ✅ Invalid API configurations
- ✅ Parsing errors

Each error provides helpful troubleshooting tips to guide you toward a solution.

## 📦 Dependencies

Core dependencies:
- `langchain` - LLM orchestration framework
- `pydantic` - Data validation and schemas
- `rich` - Beautiful CLI interface
- `duckduckgo-search` - Search tool for attractions
- `markdown2` & `reportlab` - Export functionality

See `requirements.txt` for the complete list.

## 🎯 Development Roadmap

- [x] Phase 1: Setup & Core Structure
- [x] Phase 2: Natural Language Understanding
- [x] Phase 3: Tools & Data Integration
- [x] Phase 4: Agent Logic & Orchestration
- [x] Phase 5: Interface & Polishing
  - [x] CLI with Rich
  - [x] Error handling
  - [x] Activity validation
- [x] Phase 6: Web UI ✨ **NEW!**
  - [x] Streamlit web interface with animations
  - [x] Beautiful gradient design & custom CSS
  - [x] Interactive forms & day cards
  - [x] Export to PDF/Markdown from web
  - [ ] User authentication (Future)
  - [ ] Saved itineraries (Future)

## 🤝 Contributing

This project was developed as part of a hackathon. Contributions are welcome!

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Search powered by DuckDuckGo
- LLM support for Ollama, Google Gemini, and OpenAI

## 📞 Support

For issues or questions, please check:
1. Your `.env` configuration
2. API key validity
3. Network connectivity
4. Model availability

## 🔍 Troubleshooting

### Common Issues

**"Could not understand the request"**
- Provide more details: destination, duration, budget, and interests
- Example: "Plan a 3-day trip to Paris for a couple interested in art and food. Medium budget."

**"Failed to generate itinerary"**
- Check your internet connection
- Verify API keys in `.env` file
- Ensure the selected model is available
- Check if you've exceeded API rate limits

**"PDF export failed"**
- Ensure `reportlab` is installed: `pip install reportlab`
- Check that the output directory exists and is writable

---

**Happy Travels! 🌎✈️**

*Made with ❤️ for the TCS Hackathon*
