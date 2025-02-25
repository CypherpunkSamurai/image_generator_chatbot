from typing import List
from langchain_core.messages import AIMessage, HumanMessage

from db import DatabaseMemory
from llm import LLMManager

class Chatbot:
    def __init__(self, model_name: str = None, conversation_id: str = "default"):
        self.conversation_id = conversation_id
        self.memory = DatabaseMemory()
        self.llm = LLMManager(model_name)
        
    def _get_chat_history(self) -> List:
        history = self.memory.get_conversation_history(self.conversation_id)
        messages = []
        for msg in history:
            if msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                messages.append(AIMessage(content=msg["content"]))
        return messages
    
    def chat(self, user_input: str) -> str:
        # Save user message to database
        self.memory.save_message(self.conversation_id, "human", user_input)
        
        # Get response from the model
        response = self.llm.chain.invoke({
            "history": self._get_chat_history(),
            "input": [HumanMessage(content=user_input)]
        })
        
        # Save AI response to database
        self.memory.save_message(self.conversation_id, "ai", response.content)
        
        return response.content

def main():
    # Create chatbot instance
    chatbot = Chatbot()
    
    print("Chatbot initialized! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.chat(user_input)
        print(f"\nAI: {response}")

if __name__ == "__main__":
    main()
