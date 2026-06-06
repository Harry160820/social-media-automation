import logging
import os
from datetime import datetime

# Create logs directory
LOGS_DIR = "/home/azureuser/social-media-automation/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def get_logger(name):
    """Get configured logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler — saves all logs
    log_file = f"{LOGS_DIR}/{name}_{datetime.now().strftime('%Y%m')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler — shows important logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s — %(name)s — %(levelname)s — %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Alert system
def send_alert(subject, message):
    """Send email alert on failure"""
    import smtplib
    from email.mime.text import MIMEText
    from dotenv import load_dotenv
    
    load_dotenv('/home/azureuser/social-media-automation/.env')
    
    GMAIL_USER = os.getenv('GMAIL_USER')
    GMAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
    
    msg = MIMEText(f"""
     SYSTEM ALERT
    
    Subject: {subject}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    {message}
    
    — Social Media Automation System
    """)
    
    msg['Subject'] = f" Alert: {subject}"
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
        server.quit()
        print(f" Alert sent: {subject}")
    except Exception as e:
        print(f" Alert failed: {e}")

if __name__ == "__main__":
    logger = get_logger("test")
    logger.info("Logger working!")
    logger.warning("This is a warning!")
    logger.error("This is an error!")
    print(" Logger test complete!")
