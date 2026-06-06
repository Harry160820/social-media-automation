import feedparser
import requests
import json
import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('/home/azureuser/social-media-automation/.env')

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['social_media_db']
collection = db['competitor_insights']

# Ollama config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# Competitor RSS feeds (Education niche)
COMPETITOR_FEEDS = [
    {
        "name": "Coursera Blog",
        "url": "https://blog.coursera.org/feed/",
        "platform": "blog"
    },
    {
        "name": "edX Blog",
        "url": "https://www.edx.org/blog/feed",
        "platform": "blog"
    },
    {
        "name": "Khan Academy Blog",
        "url": "https://blog.khanacademy.org/feed/",
        "platform": "blog"
    },
    {
        "name": "TechCrunch Education",
        "url": "https://techcrunch.com/tag/education/feed/",
        "platform": "news"
    },
    {
        "name": "eLearn Magazine",
        "url": "https://elearnmag.acm.org/rss.xml",
        "platform": "magazine"
    }
]

def fetch_competitor_posts(feed):
    """Fetch posts from competitor RSS feed"""
    try:
        print(f"Fetching: {feed['name']}...")
        parsed = feedparser.parse(feed['url'])
        
        posts = []
        for entry in parsed.entries[:5]:  # Get latest 5 posts
            posts.append({
                "title": entry.get('title', ''),
                "summary": entry.get('summary', '')[:500],
                "link": entry.get('link', ''),
                "published": entry.get('published', ''),
                "source": feed['name']
            })
        
        print(f" Got {len(posts)} posts from {feed['name']}")
        return posts
    
    except Exception as e:
        print(f" Error fetching {feed['name']}: {e}")
        return []

def analyze_with_llama(posts):
    """Send posts to LLaMA for analysis"""
    print("\nAnalyzing with LLaMA 3...")
    
    posts_text = json.dumps(posts, indent=2)
    
    prompt = f"""Analyze these competitor education brand posts and identify patterns.
Return ONLY valid JSON with no extra text.

{{
  "top_hooks": ["hook1", "hook2", "hook3"],
  "content_formats": ["format1", "format2", "format3"],
  "trending_topics": ["topic1", "topic2", "topic3"],
  "engagement_triggers": ["trigger1", "trigger2", "trigger3"],
  "posting_patterns": "description of when and how often they post",
  "opportunities": ["opportunity1", "opportunity2"],
  "recommended_topics": ["topic1", "topic2", "topic3"]
}}

Posts to analyze:
{posts_text[:3000]}"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    })
    
    if response.status_code == 200:
        raw = response.json()["response"]
        
        # Parse JSON
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_str = raw[start:end]
        
        try:
            insights = json.loads(json_str)
            print(" Analysis complete!")
            return insights
        except:
            print(" Could not parse JSON, returning raw")
            return {"raw_analysis": raw}
    else:
        print(f" LLaMA error: {response.status_code}")
        return None

def save_to_mongodb(insights, posts):
    """Save insights to MongoDB"""
    document = {
        "analyzed_at": datetime.now().isoformat(),
        "total_posts_analyzed": len(posts),
        "insights": insights,
        "raw_posts": posts,
        "week": datetime.now().strftime("%Y-W%V")
    }
    
    result = collection.insert_one(document)
    print(f" Saved to MongoDB: {result.inserted_id}")
    return str(result.inserted_id)

def send_weekly_summary(insights):
    """Send weekly insights email"""
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    APPROVAL_EMAIL = os.getenv('APPROVAL_EMAIL')
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f" Weekly Competitor Analysis — {datetime.now().strftime('%B %d, %Y')}"
    msg['From'] = GMAIL_USER
    msg['To'] = APPROVAL_EMAIL
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        
        <h2 style="color: #333;"> Weekly Competitor Intelligence Report</h2>
        <p style="color: #666;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        
        <hr/>
        
        <h3 style="color: #6366F1;">🎣 Top Hooks Being Used</h3>
        <ul>
            {''.join([f"<li>{hook}</li>" for hook in insights.get('top_hooks', [])])}
        </ul>
        
        <h3 style="color: #0EA5E9;"> Popular Content Formats</h3>
        <ul>
            {''.join([f"<li>{fmt}</li>" for fmt in insights.get('content_formats', [])])}
        </ul>
        
        <h3 style="color: #10B981;"> Trending Topics</h3>
        <ul>
            {''.join([f"<li>{topic}</li>" for topic in insights.get('trending_topics', [])])}
        </ul>
        
        <h3 style="color: #F59E0B;"> Opportunities for Us</h3>
        <ul>
            {''.join([f"<li>{opp}</li>" for opp in insights.get('opportunities', [])])}
        </ul>
        
        <h3 style="color: #8B5CF6;"> Recommended Topics for Next Week</h3>
        <ul>
            {''.join([f"<li>{topic}</li>" for topic in insights.get('recommended_topics', [])])}
        </ul>
        
        <hr/>
        
        <p style="color: #999; font-size: 12px;">
            Social Media Automation System — Hari Om
        </p>
        
    </body>
    </html>
    """
    
    msg.attach(MIMEText(html, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, APPROVAL_EMAIL, msg.as_string())
        server.quit()
        print(" Weekly summary email sent!")
        return True
    except Exception as e:
        print(f" Email failed: {e}")
        return False

def main():
    print("="*50)
    print(" COMPETITOR ANALYSIS SYSTEM")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Fetch all competitor posts
    all_posts = []
    for feed in COMPETITOR_FEEDS:
        posts = fetch_competitor_posts(feed)
        all_posts.extend(posts)
    
    print(f"\n Total posts collected: {len(all_posts)}")
    
    if not all_posts:
        print(" No posts collected!")
        return
    
    # Analyze with LLaMA
    insights = analyze_with_llama(all_posts)
    
    if not insights:
        print(" Analysis failed!")
        return
    
    # Save to MongoDB
    doc_id = save_to_mongodb(insights, all_posts)
    
    # Print insights
    print("\n" + "="*50)
    print(" KEY INSIGHTS")
    print("="*50)
    print(f"Top Hooks: {insights.get('top_hooks', [])}")
    print(f"Trending Topics: {insights.get('trending_topics', [])}")
    print(f"Opportunities: {insights.get('opportunities', [])}")
    
    # Send weekly email
    send_weekly_summary(insights)
    
    print("\n Competitor analysis complete!")
    client.close()

if __name__ == "__main__":
    main()
