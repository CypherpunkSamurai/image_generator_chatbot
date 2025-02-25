from typing import List, Optional
from langchain_core.messages import AIMessage, HumanMessage

from db import DatabaseMemory
from llm import LLMManager
from image_api import ImageGenerator

class Chatbot:
    def __init__(self, model_name: str = None, conversation_id: str = "default"):
        self.conversation_id = conversation_id
        self.memory = DatabaseMemory()
        self.llm = LLMManager(model_name)
        self.image_generator = ImageGenerator()
    
    def _get_chat_history(self) -> List:
        history = self.memory.get_conversation_history(self.conversation_id)
        messages = []
        for msg in history:
            if msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                messages.append(AIMessage(content=msg["content"]))
        return messages
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """Generate an image using DALL-E"""
        return self.image_generator.generate_image(prompt, size)
    
    def chat(self, user_input: str) -> str:
        # Save user message to database
        self.memory.save_message(self.conversation_id, "human", user_input)
        
        # Check if this is an image generation request
        if user_input.lower().startswith("generate image:"):
            prompt = user_input[len("generate image:"):].strip()
            image_url = self.generate_image(prompt)
            response = f"Here's your generated image: {image_url}" if image_url else "Sorry, I couldn't generate the image."
        else:
            # Get response from the model
            response = self.llm.chain.invoke({
                "history": self._get_chat_history(),
                "input": [HumanMessage(content=user_input)]
            })
            response = response.content
        
        # Save AI response to database
        self.memory.save_message(self.conversation_id, "ai", response)
        
        return response

def main():
    # Create chatbot instance
    chatbot = Chatbot()
    
    print("Chatbot initialized! Type 'quit' to exit.")
    print("To generate images, start your message with 'generate image:'")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            break
            
        response = chatbot.chat(user_input)
        print(f"\nAI: {response}")

if __name__ == "__main__":
    main()
