import requests
import json
import os
from datetime import datetime

# Config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
PROMPTS_DIR = "/home/azureuser/social-media-automation/prompts"
SCRIPTS_DIR = "/home/azureuser/social-media-automation/scripts"
OUTPUT_DIR = "/home/azureuser/social-media-automation/output"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_prompt():
    with open(f"{PROMPTS_DIR}/content_prompt.txt", "r") as f:
        return f.read()

def load_source_material():
    with open(f"{SCRIPTS_DIR}/source_material.txt", "r") as f:
        return f.read()

def generate_content(source_material):
    prompt = load_prompt()
    prompt = prompt.replace("{{SOURCE_MATERIAL}}", source_material)
    
    print("Sending to LLaMA 3...")
    
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    })
    
    if response.status_code == 200:
        raw = response.json()["response"]
        print("Raw response received!")
        return raw
    else:
        print(f"Error: {response.status_code}")
        return None

def parse_content(raw_response):
    try:
        # Find JSON in response
        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1
        json_str = raw_response[start:end]
        return json.loads(json_str)
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def save_content(content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{OUTPUT_DIR}/content_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(content, f, indent=2)
    
    print(f"Content saved to: {filename}")
    return filename

def main():
    print("=== Social Media Content Generator ===")
    print(f"Time: {datetime.now()}")
    print("="*40)
    
    # Load source material
    source = load_source_material()
    print(f"Source material loaded: {len(source)} characters")
    
    # Generate content
    raw = generate_content(source)
    if not raw:
        print("Failed to generate content")
        return
    
    # Parse content
    content = parse_content(raw)
    if not content:
        print("Failed to parse content")
        print("Raw response:", raw)
        return
    
    # Save content
    filename = save_content(content)
    
    # Print preview
    print("\n=== CONTENT PREVIEW ===")
    print("\n INSTAGRAM:")
    print(content.get("instagram", {}).get("caption", "N/A"))
    
    print("\n LINKEDIN:")
    print(content.get("linkedin", {}).get("post", "N/A"))
    
    print("\n TIKTOK HOOK:")
    print(content.get("tiktok", {}).get("hook", "N/A"))
    
    print("\n YOUTUBE TITLE:")
    print(content.get("youtube", {}).get("title", "N/A"))
    
    print("\n FACEBOOK:")
    print(content.get("facebook", {}).get("post", "N/A"))
    
    print("\n Done!")

if __name__ == "__main__":
    main()
