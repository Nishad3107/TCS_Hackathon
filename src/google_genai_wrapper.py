"""
Wrapper for native Google GenAI SDK to work with LangChain
"""
from google import genai
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from typing import List, Optional, Any
import os


class NativeGoogleGenAI(BaseChatModel):
    """Wrapper for native Google GenAI SDK"""
    
    def __init__(self, model: str = "gemini-2.0-flash", api_key: str = "", temperature: float = 0.7, **kwargs):
        super().__init__(**kwargs)
        self._model = model
        self._api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self._temperature = temperature
        
        # Set environment variable for the client
        if self._api_key:
            os.environ["GEMINI_API_KEY"] = self._api_key
        
        self._client = genai.Client()
    
    @property
    def model(self):
        return self._model
    
    @property
    def api_key(self):
        return self._api_key
    
    @property
    def temperature(self):
        return self._temperature
    
    @property
    def client(self):
        return self._client
    
    def _convert_messages_to_content(self, messages: List[BaseMessage]) -> str:
        """Convert LangChain messages to a single content string"""
        content_parts = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                content_parts.append(f"System: {msg.content}")
            elif isinstance(msg, HumanMessage):
                content_parts.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                content_parts.append(f"Assistant: {msg.content}")
            else:
                content_parts.append(msg.content)
        return "\n".join(content_parts)
    
    def _generate(self, messages: List[BaseMessage], **kwargs) -> Any:
        """Generate response using native Google GenAI SDK"""
        content = self._convert_messages_to_content(messages)
        
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=content
            )
            return AIMessage(content=response.text)
        except Exception as e:
            raise Exception(f"Google GenAI API Error: {str(e)}")
    
    def invoke(self, input_data, **kwargs):
        """Invoke the model - compatible with LangChain interface"""
        # Handle both string and message list inputs
        if isinstance(input_data, str):
            messages = [HumanMessage(content=input_data)]
        elif isinstance(input_data, list):
            messages = input_data
        else:
            messages = [HumanMessage(content=str(input_data))]
        
        return self._generate(messages, **kwargs)
    
    @property
    def _llm_type(self) -> str:
        return "google-genai-native"
