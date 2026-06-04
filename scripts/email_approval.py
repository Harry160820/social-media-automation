import smtplib
import json
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

# Load credentials
load_dotenv('/home/azureuser/social-media-automation/.env')

GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
APPROVAL_EMAIL = os.getenv('APPROVAL_EMAIL')

def send_approval_email(content, content_id):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f" Content Approval Required — {content_id}"
    msg['From'] = GMAIL_USER
    msg['To'] = APPROVAL_EMAIL

    # Email body
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        
        <h2 style="color: #333;"> Social Media Content Ready for Approval</h2>
        <p style="color: #666;">Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        
        <hr/>
        
        <h3 style="color: #E1306C;"> Instagram</h3>
        <p>{content.get('instagram', {}).get('caption', 'N/A')}</p>
        <p><strong>Hashtags:</strong> {' '.join(content.get('instagram', {}).get('hashtags', []))}</p>
        <p><strong>CTA:</strong> {content.get('instagram', {}).get('cta', 'N/A')}</p>
        
        <hr/>
        
        <h3 style="color: #0077B5;"> LinkedIn</h3>
        <p>{content.get('linkedin', {}).get('post', 'N/A')}</p>
        <p><strong>CTA:</strong> {content.get('linkedin', {}).get('cta', 'N/A')}</p>
        
        <hr/>
        
        <h3 style="color: #000000;"> TikTok</h3>
        <p><strong>Hook:</strong> {content.get('tiktok', {}).get('hook', 'N/A')}</p>
        <p><strong>Script:</strong> {content.get('tiktok', {}).get('script', 'N/A')}</p>
        
        <hr/>
        
        <h3 style="color: #FF0000;"> YouTube</h3>
        <p><strong>Title:</strong> {content.get('youtube', {}).get('title', 'N/A')}</p>
        <p><strong>Description:</strong> {content.get('youtube', {}).get('description', 'N/A')}</p>
        
        <hr/>
        
        <h3 style="color: #1877F2;"> Facebook</h3>
        <p>{content.get('facebook', {}).get('post', 'N/A')}</p>
        
        <hr/>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="http://40.81.25.135:5678/webhook/7fa7d660-3ce8-4a84-93ed-8e7c7c31e93d/approve/{content_id}" 
               style="background: #28a745; color: white; padding: 15px 30px; 
                      text-decoration: none; border-radius: 5px; margin: 10px;
                      font-size: 16px;">
                APPROVE
            </a>
            &nbsp;&nbsp;&nbsp;
            <a href="http://40.81.25.135:5678/webhook/e2bf5238-f93d-487a-9b6c-e1dcd3a98e5a/reject/{content_id}"
               style="background: #dc3545; color: white; padding: 15px 30px;
                      text-decoration: none; border-radius: 5px; margin: 10px;
                      font-size: 16px;">
                REJECT
            </a>
        </div>
        
        <p style="color: #999; font-size: 12px; text-align: center;">
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
        print(f" Approval email sent to {APPROVAL_EMAIL}")
        return True
    except Exception as e:
        print(f" Email failed: {e}")
        return False

def main():
    # Load latest generated content
    output_dir = "/home/azureuser/social-media-automation/output"
    files = sorted(os.listdir(output_dir))
    
    if not files:
        print("No content files found")
        return
    
    latest_file = files[-1]
    content_id = latest_file.replace(".json", "")
    
    with open(f"{output_dir}/{latest_file}", "r") as f:
        content = json.load(f)
    
    print(f"Sending approval email for: {content_id}")
    send_approval_email(content, content_id)

if __name__ == "__main__":
    main()
