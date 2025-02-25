# Mock Image API
# Will Later be replaced with actual image generation code
import httpx
import os
from typing import Optional
from dotenv import load_dotenv
from langchain_community.tools.openai_dalle_image_generation.tool import OpenAIDALLEImageGenerationTool
from langchain_core.tools import Tool

class ImageGenerator:
    def __init__(self):
        load_dotenv()
        self.dalle_tool = OpenAIDALLEImageGenerationTool(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_base=os.getenv("OPENAI_BASE_URL")
        )
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """
        Generate an image using DALL-E based on the given prompt.
        
        Args:
            prompt (str): The text description of the image to generate
            size (str): Image size, one of "1024x1024", "512x512", or "256x256"
            
        Returns:
            str: URL of the generated image, or None if generation failed
        """
        try:
            result = self.dalle_tool.invoke({"text": prompt, "size": size})
            return result
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def get_tool(self) -> Tool:
        """
        Get the image generation tool for use in LangChain.
        """
        return self.dalle_tool

def generate_image(prompt: str) -> httpx.Response:
    # Mock image generation code
    print(f"Generating image for prompt: {prompt}")
    # returns url to image
    return httpx.get("https://picsum.photos/200/200")
