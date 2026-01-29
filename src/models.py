import os
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

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
            # Google Gemini
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables.")
            return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
            
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
