import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate

class LLMManager:
    def __init__(self, model_name: str = None):
        # Load environment variables
        load_dotenv()
        
        # Use model from environment variable if not specified
        if model_name is None:
            model_name = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")
        
        # Initialize the chat model with configurable base URL
        self.chat_model = ChatOpenAI(
            model_name=model_name,
            temperature=0.7,
            openai_api_base=os.getenv("OPENAI_BASE_URL"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create the chat prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a helpful and friendly AI assistant. Answer questions clearly and concisely."),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="input"),
        ])
        
        # Create the conversation chain
        self.chain = (
            {
                "history": lambda x: x["history"],
                "input": lambda x: x["input"],
            }
            | self.prompt
            | self.chat_model
        )
