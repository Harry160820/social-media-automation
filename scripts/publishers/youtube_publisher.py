import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

YOUTUBE_ACCESS_TOKEN = os.getenv('YOUTUBE_ACCESS_TOKEN')

def post_youtube_community(title, description, tags):
    """Post to YouTube community tab"""
    print(" Publishing to YouTube...")
    
    url = "https://www.googleapis.com/youtube/v3/communityPosts"
    headers = {
        "Authorization": f"Bearer {YOUTUBE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "snippet": {
            "type": "text",
            "textOriginal": f"{title}\n\n{description}\n\nTags: {', '.join(tags)}"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print(" Published to YouTube!")
        return True
    else:
        print(f" YouTube error: {response.json()}")
        return False

def create_youtube_video_metadata(title, description, tags):
    """Prepare video metadata for upload"""
    return {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Education category
        },
        "status": {
            "privacyStatus": "public"
        }
    }

# Mock function for demo
def mock_post_to_youtube(title, description, tags):
    print(" [DEMO] Publishing to YouTube...")
    print(f"Title: {title}")
    print(f"Description: {description[:50]}...")
    print(f"Tags: {', '.join(tags[:3])}...")
    print(" [DEMO] Successfully posted to YouTube!")
    return True

if __name__ == "__main__":
    mock_post_to_youtube(
        "Why Online Learning is the Future | 2026",
        "In this video we explore why online learning...",
        ["OnlineLearning", "Education", "AI"]
    )
