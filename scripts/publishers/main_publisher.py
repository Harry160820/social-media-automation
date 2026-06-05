import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

# Import all publishers
from instagram_publisher import mock_post_to_instagram
from linkedin_publisher import mock_post_to_linkedin
from youtube_publisher import mock_post_to_youtube
from facebook_publisher import mock_post_to_facebook

def publish_all(content_file):
    """Publish content to all platforms"""
    
    print("="*50)
    print(" SOCIAL MEDIA AUTO-PUBLISHER")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Load content
    with open(content_file, 'r') as f:
        content = json.load(f)
    
    results = {}
    
    # Instagram
    instagram = content.get('instagram', {})
    results['instagram'] = mock_post_to_instagram(
        instagram.get('caption', ''),
        instagram.get('hashtags', [])
    )
    
    print()
    
    # LinkedIn
    linkedin = content.get('linkedin', {})
    results['linkedin'] = mock_post_to_linkedin(
        linkedin.get('post', ''),
        linkedin.get('cta', '')
    )
    
    print()
    
    # YouTube
    youtube = content.get('youtube', {})
    results['youtube'] = mock_post_to_youtube(
        youtube.get('title', ''),
        youtube.get('description', ''),
        youtube.get('tags', [])
    )
    
    print()
    
    # Facebook
    facebook = content.get('facebook', {})
    results['facebook'] = mock_post_to_facebook(
        facebook.get('post', ''),
        facebook.get('cta', '')
    )
    
    # Summary
    print()
    print("="*50)
    print(" PUBLISHING SUMMARY")
    print("="*50)
    for platform, success in results.items():
        status = " Published" if success else " Failed"
        print(f"{platform.capitalize()}: {status}")
    
    # Save results
    output_dir = "/home/azureuser/social-media-automation/output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"{output_dir}/published_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "published_at": datetime.now().isoformat(),
            "content_file": content_file,
            "results": results
        }, f, indent=2)
    
    print(f"\n Results saved to: {results_file}")
    return results

if __name__ == "__main__":
    # Get latest content file
    output_dir = "/home/azureuser/social-media-automation/output"
    files = [f for f in sorted(os.listdir(output_dir)) if f.startswith('content_')]
    
    if not files:
        print(" No content files found. Run content_generator.py first!")
        sys.exit(1)
    
    latest = f"{output_dir}/{files[-1]}"
    print(f"Using content file: {latest}")
    publish_all(latest)
