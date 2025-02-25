# Mock Image API
# Will Later be replaced with actual image generation code
import httpx

def generate_image(prompt: str) -> httpx.Response:
    # Mock image generation code
    print(f"Generating image for prompt: {prompt}")
    # retuns url to image
    return httpx.get("https://picsum.photos/200/200")
