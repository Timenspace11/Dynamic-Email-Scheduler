

import os
import pandas as pd
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from getpass import getpass
from apscheduler.schedulers.background import BackgroundScheduler
import time
import google.generativeai as genai
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime


# Assuming the Flask app and database are in the same script
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
db = SQLAlchemy(app)

class EmailStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    response_received = db.Column(db.Boolean, default=False)
    message_id = db.Column(db.String(100), unique=True, nullable=True)  # Mailgun Message ID

# Ensure tables are created
with app.app_context():
    db.create_all()

# Configure Google Generative AI
GOOGLE_API_KEY = 'AIzaSyAVQ0jp9tYDMtTAriRYQfYyzro_FyLxGgk'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Mailgun configuration
MAILGUN_DOMAIN = "sandboxe007be8ff90748f0959dd49c96ba67c9.mailgun.org"  # Your Mailgun domain
MAILGUN_API_KEY =  input("Enter Your Mailgun API Key: ") 
# getpass("Enter Your Mailgun API Key: ")  would have used it but For getpass I have to create a env file 

# Email Credentials
sender_email = input("Enter Your Verified Email ID: ")

# Read CSV file
df = pd.read_csv(r"C:\Users\Thakur\sample_data1.csv")
receivers_email = df["EMAIL_ID"].values
attach_files = df["Files_to_be_attached"].values
names = df["NAME"].values

sub = "Test Mail"
zipped = zip(receivers_email, attach_files, names)

# Generate content using Google Generative AI
def generate_email_content(name):
    prompt = f"Write a friendly email message for {name} with a greeting and closing, Explain why understanding global warming is important, covering its causes, main effects, and ways we can address it together as a society."
    response = model.generate_content(prompt)
    return response.text

# Send email using Mailgun
def send_email_with_mailgun(email, content, attachment_path, file_id):
    # Mailgun API endpoint
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    # Prepare data for the request
    data = {
        "from": f"Your Name <{sender_email}>",
        "to": email,
        "subject": sub,
        "text": content
    }

    # Prepare attachment
    files = []
    try:
        with open(attachment_path, 'rb') as f:
            files.append(("attachment", (f"{file_id}.pdf", f.read())))
    except FileNotFoundError:
        print(f"Attachment {attachment_path} not found. Skipping this email.")
        return

    # Send the request to Mailgun API
    try:
        response = requests.post(
            url,
            auth=("api", MAILGUN_API_KEY),
            data=data,
            files=files
        )
        response.raise_for_status()
        message_id = response.json().get('id')
        print(f"Email sent to {email} with Mailgun ID: {message_id}")

        # Log the email in the database
        email_status = EmailStatus(
            recipient=email,
            status="sent",
            sent_at= datetime.utcnow(),
            message_id=message_id
        )
        db.session.add(email_status)
        db.session.commit()
    except requests.exceptions.RequestException as e:
        print(f"Error sending email to {email}: {e}")
        # Log the failed email
        email_status = EmailStatus(
            recipient=email,
            status="failed",
            message_id=None  # No message_id if failed to send
        )
        db.session.add(email_status)
        db.session.commit()

# Schedule and throttle emails
scheduler = BackgroundScheduler()

def send_scheduled_emails():
    for email, file_id, name in zipped:
        # Generate email content using LLM
        email_body = generate_email_content(name)

        # Prepare attachment file path
        attachment_path = fr"C:\Users\Thakur\Desktop\classical and fuzzy relations.pdf"
        
        # Send email with Mailgun
        send_email_with_mailgun(email, email_body, attachment_path, file_id)
        
        # Throttle emails by adding a delay
        time.sleep(10)  # Adjust delay as needed to control sending rate

# Schedule job for every day at a specific time (e.g., 9:00 AM)
scheduler.add_job(send_scheduled_emails, 'cron', hour=8, minute=10)
scheduler.start()

print("Scheduler started. Emails will be sent as per the schedule.")
