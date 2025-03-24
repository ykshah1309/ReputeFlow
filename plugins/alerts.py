import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class AlertSystem:
    def __init__(self):
        self.email = os.getenv("ALERT_EMAIL")
        self.password = os.getenv("ALERT_PASSWORD")
    
    def send_email(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = self.email
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.email, msg.as_string())
            print("Alert email sent successfully")
        except Exception as e:
            print(f"Failed to send alert: {e}")