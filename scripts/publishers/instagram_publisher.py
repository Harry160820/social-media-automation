import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

def create_media_container(caption, image_url):
    """Step 1 — Upload media container"""
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    
    payload = {
        "caption": caption,
        "image_url": image_url,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        print(f" Media container created: {result['id']}")
        return result["id"]
    else:
        print(f" Error: {result}")
        return None

def publish_media(container_id):
    """Step 2 — Publish the container"""
    url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    
    payload = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        print(f" Published to Instagram! Post ID: {result['id']}")
        return result["id"]
    else:
        print(f" Publish error: {result}")
        return None

def post_to_instagram(caption, hashtags, image_url):
    """Main function to post to Instagram"""
    print(" Publishing to Instagram...")
    
    # Combine caption with hashtags
    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
    
    # Step 1: Create container
    container_id = create_media_container(full_caption, image_url)
    if not container_id:
        return False
    
    # Step 2: Publish
    post_id = publish_media(container_id)
    return post_id is not None

# Mock function for demo
def mock_post_to_instagram(caption, hashtags):
    print(" [DEMO] Publishing to Instagram...")
    print(f"Caption: {caption[:50]}...")
    print(f"Hashtags: {' '.join(hashtags[:3])}...")
    print(" [DEMO] Successfully posted to Instagram!")
    return True

if __name__ == "__main__":
    # Test with mock
    mock_post_to_instagram(
        "Transform your future with online learning!",
        ["#OnlineLearning", "#Education", "#Growth"]
    )
