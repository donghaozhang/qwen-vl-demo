from PIL import Image
import requests
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def process_vision_info(messages):
    """
    Process the vision information from messages to extract images and videos.
    
    Args:
        messages: List of message dictionaries with content
        
    Returns:
        tuple: (image_inputs, video_inputs)
    """
    image_inputs = []
    video_inputs = []
    
    for message in messages:
        if "content" in message and isinstance(message["content"], list):
            for content in message["content"]:
                if content.get("type") == "image" and "image" in content:
                    image = content["image"]
                    # Handle image which can be a path, URL, or PIL Image
                    if isinstance(image, str):
                        # If it's a URL
                        if image.startswith(("http://", "https://")):
                            try:
                                logger.info(f"Downloading image from URL: {image}")
                                response = requests.get(image, timeout=10)
                                response.raise_for_status()
                                image = Image.open(BytesIO(response.content))
                                logger.info("Image downloaded successfully")
                            except Exception as e:
                                logger.error(f"Failed to download image from URL: {e}")
                                continue
                        # If it's a path to a local file
                        else:
                            try:
                                logger.info(f"Loading image from path: {image}")
                                image = Image.open(image)
                                logger.info("Image loaded successfully")
                            except Exception as e:
                                logger.error(f"Failed to open image file: {e}")
                                continue
                    
                    # Verify that we have a valid PIL Image
                    if not isinstance(image, Image.Image):
                        logger.error(f"Invalid image type: {type(image)}")
                        continue
                        
                    image_inputs.append(image)
                    
                elif content.get("type") == "video" and "video" in content:
                    video_inputs.append(content["video"])
    
    return image_inputs, video_inputs