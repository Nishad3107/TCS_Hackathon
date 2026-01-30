import os
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

# Try new Google GenAI SDK first, fallback to LangChain
try:
    from google import genai as google_genai
    USE_NATIVE_GENAI = True
except ImportError:
    USE_NATIVE_GENAI = False

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    USE_LANGCHAIN_GENAI = True
except ImportError:
    USE_LANGCHAIN_GENAI = False

# Import our native wrapper
if USE_NATIVE_GENAI:
    from google_genai_wrapper import NativeGoogleGenAI

class ModelFactory:
    @staticmethod
    def get_model(model_name: str = None) -> BaseChatModel:
        """
        Returns a ChatModel instance based on the configuration or name.
        """
        model_name = model_name or os.getenv("MODEL_NAME", "llama3")
        
        print(f"Loading model: {model_name}...")

        if "llama" in model_name or "mistral" in model_name or "gemma" in model_name:
            # Assume Ollama for these local models
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            return ChatOllama(model=model_name, base_url=base_url)
        
        elif "gemini" in model_name:
            # Google Gemini - Try native SDK first
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not found in environment variables.")
            
            # Prefer native Google GenAI SDK (more compatible with latest API)
            if USE_NATIVE_GENAI:
                print(f"Using native Google GenAI SDK for {model_name}")
                return NativeGoogleGenAI(
                    model=model_name,
                    api_key=api_key,
                    temperature=0.7
                )
            # Fallback to LangChain integration
            elif USE_LANGCHAIN_GENAI:
                print(f"Using LangChain Google GenAI for {model_name}")
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=api_key,
                    temperature=0.7,
                    convert_system_message_to_human=True
                )
            else:
                raise ValueError("No Google GenAI integration available. Install: pip install google-genai")
            
        elif "gpt" in model_name:
            # OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            return ChatOpenAI(model=model_name, api_key=api_key)
            
        else:
            # Default to Ollama if unknown, or raise error
            print(f"Warning: Unknown model provider for '{model_name}'. Defaulting to Ollama.")
            return ChatOllama(model=model_name)
