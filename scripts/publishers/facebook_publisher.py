import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')

def post_to_facebook(message, cta):
    """Post to Facebook Page"""
    print(" Publishing to Facebook...")
    
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
    
    payload = {
        "message": f"{message}\n\n{cta}",
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        print(f" Published to Facebook! Post ID: {result['id']}")
        return True
    else:
        print(f" Facebook error: {result}")
        return False

# Mock function for demo
def mock_post_to_facebook(message, cta):
    print(" [DEMO] Publishing to Facebook...")
    print(f"Message: {message[:50]}...")
    print(f"CTA: {cta}")
    print(" [DEMO] Successfully posted to Facebook!")
    return True

if __name__ == "__main__":
    mock_post_to_facebook(
        "Online learning is changing lives worldwide...",
        "Like and share if you agree!"
    )
