import base64
import anthropic
from pathlib import Path

def create_image_content(image_path):
    """Create a content list entry for an image."""
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        image_title = Path(image_path).stem
        
        return [
            {
                "type": "text",
                "text": image_title
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",  # Added specific media type
                    "data": image_data
                }
            }
        ]

def process_images_with_transcript(folder_path, transcript_path, question):
    """Process multiple images and a transcript with caching support."""
    # Initialize the client with your API key
    client = anthropic.Client(api_key=os.environ.get("Anthropic_API_KEY"))
    
    # Get all image files from the folder
    image_files = sorted(Path(folder_path).glob("*.jpeg"))  # Added sorting for consistency
    
    # Prepare content list with all images
    content = []
    for image_path in image_files:
        content.extend(create_image_content(image_path))
    
    # Read the transcript file
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        # Append the transcript content to the content list
        content.append({
            "type": "text",
            "text": f"Transcript: {transcript_content}"  # Added label for clarity
        })
    except Exception as e:
        print(f"Could not read transcript file: {e}")
    
    # Add the question at the end
    content.append({
        "type": "text",
        "text": f"Question: {question}"  # Added label for clarity
    })

    try:
        # Create the message using the correct parameter structure
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            system="You are an AI assistant providing a detailed analysis of a sequence of images from a video. Images are taken at 1-second intervals. You will remember all images and hence understand the video.",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        
        return response
    except Exception as e:
        raise Exception(f"Error creating message: {e}")

def chat_with_images(folder_path, transcript_path, question):
    try:
        response = process_images_with_transcript(folder_path, transcript_path, question)
        # The response structure has changed in newer versions
        print(response.content[0].text)
    except Exception as e:
        print(f"An error occurred: {e}")

# Add imports at the top if not already present
import os
from pathlib import Path