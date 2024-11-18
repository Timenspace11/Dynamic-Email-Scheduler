!pip install apscheduler

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


# we will Configure Google Generative AI , we have to just generate the key and paste here
GOOGLE_API_KEY = getpass("Enter Your GOOGLE_API_KEY") 
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# This is Mailgun configuration
MAILGUN_DOMAIN = "sandboxe007be8ff90748f0959dd49c96ba67c9.mailgun.org" 
MAILGUN_API_KEY = getpass("Enter Your Mailgun API Key: ")

print(MAILGUN_API_KEY)

# Email Credentials of the guy who is sending emails
sender_email = input("Enter Your Verified Email ID: ")

# Read CSV file 
df = pd.read_csv(r"C:\Users\Thakur\sample_data1.csv")
receivers_email = df["EMAIL_ID"].values
attach_files = df["Files_to_be_attached"].values
names = df["NAME"].values

sub = "Test Mail"
zipped = zip(receivers_email, attach_files, names)    # using zip function here


# Generating content using Google Generative AI
def generate_email_content(name):
    prompt = f"Write a friendly email message for {name} with a greeting and closing, Explain why understanding global warming is important, covering its causes, main effects, and ways we can address it together as a society."
    response = model.generate_content(prompt)
    return response.text


# Sending email using Mailgun
def send_email_with_mailgun(email, content, attachment_path, file_id):
    # Mailgun API endpoint
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    # Preparing data for the request
    data = {
        "from": f"Mailgun Sandbox <{sender_email}>",
        "to": email,
        "subject": sub,
        "text": content
    }

    # Preparing the attachment
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
        print(f"Email sent to {email} with Mailgun ID: {response.json().get('id')}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending email to {email}: {e}")

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
        
        # adding a delay
        time.sleep(10)  # Can adjust delay as needed to control sending rate

# Schedule job for every day at a specific time
scheduler.add_job(send_scheduled_emails, 'cron', hour=8, minute=38)
scheduler.start()

print("Scheduler started. Emails will be sent as per the schedule.")
