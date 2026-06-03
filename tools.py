import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL, EMAIL_PASS, NOTIFY_EMAIL

def send_lead_email(lead_data):
    """Wasiq ko lead email bhejo"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = NOTIFY_EMAIL
        msg['Subject'] = f"🔥 New Lead — D'LO AI — {lead_data.get('business', 'Unknown')}"

        body = f"""
NAYA LEAD AA GAYA! 🔥

━━━━━━━━━━━━━━━━━━━━━━
LEAD DETAILS:
━━━━━━━━━━━━━━━━━━━━━━

Naam:         {lead_data.get('naam', 'N/A')}
Business:     {lead_data.get('business', 'N/A')}
Business Type:{lead_data.get('business_type', 'N/A')}
Masla:        {lead_data.get('masla', 'N/A')}
Contact:      {lead_data.get('contact', 'N/A')}
Best Time:    {lead_data.get('best_time', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━
CONVERSATION SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━
{lead_data.get('summary', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━
D'LO AI Sales Agent
        """

        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        return True

    except Exception as e:
        print(f"Email error: {e}")
        return False

def extract_lead_info(conversation_history):
    """Conversation se lead info extract karo"""
    lead = {
        "naam": "N/A",
        "business": "N/A", 
        "business_type": "N/A",
        "masla": "N/A",
        "contact": "N/A",
        "best_time": "N/A",
        "summary": "N/A"
    }
    return lead

def format_lead_message(lead_data):
    """Lead ka clean message banao"""
    return f"""
🔥 New Lead!
Naam: {lead_data.get('naam', 'N/A')}
Business: {lead_data.get('business', 'N/A')}
Masla: {lead_data.get('masla', 'N/A')}
Contact: {lead_data.get('contact', 'N/A')}
    """.strip()