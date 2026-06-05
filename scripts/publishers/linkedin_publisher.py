import requests
import os
import json
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_PERSON_ID = os.getenv('LINKEDIN_PERSON_ID')
LINKEDIN_ORG_ID = os.getenv('LINKEDIN_ORG_ID')

def get_person_id():
    """Get LinkedIn Person ID"""
    url = "https://api.linkedin.com/v2/me"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    return result.get("id")

def post_to_linkedin(post_text, cta):
    """Post to LinkedIn"""
    print(" Publishing to LinkedIn...")
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    payload = {
        "author": f"urn:li:person:{LINKEDIN_PERSON_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"{post_text}\n\n{cta}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print(f" Published to LinkedIn!")
        return True
    else:
        print(f" LinkedIn error: {response.json()}")
        return False

# Mock function for demo
def mock_post_to_linkedin(post_text, cta):
    print(" [DEMO] Publishing to LinkedIn...")
    print(f"Post: {post_text[:50]}...")
    print(f"CTA: {cta}")
    print(" [DEMO] Successfully posted to LinkedIn!")
    return True

if __name__ == "__main__":
    mock_post_to_linkedin(
        "The future of education is online. Here's why...",
        "Follow for more AI and education insights!"
    )
