# Email Scheduling and Content Generation Using Google Generative AI

## Project Overview

This project automates the process of sending personalized emails using **Google Generative AI** for dynamic content generation and **Mailgun API** for email delivery. The emails are scheduled and throttled 
to control the rate of sending. The system reads recipient information (email addresses, names, and attachment files) from a CSV file, generates email content using AI, and sends emails with attachments.

## Features

- **Email Content Generation**: Uses Google Generative AI to generate personalized content for each recipient.
- **Email Sending**: Sends emails using Mailgun API with attachments.
- **Scheduling**: Emails are sent on a predefined schedule using **apscheduler**.
- **Throttling**: Introduces a delay between each email to control the rate of sending.


## Prerequisites

Before running the project, ensure that you have the following installed:

- **Python 3.x** 
- **Pip** for installing dependencies
- **Google Generative AI API Key** (You will need to obtain an API key from [Google Cloud](https://cloud.google.com/))
- **Mailgun API Key** (Sign up at [Mailgun](https://www.mailgun.com/) to get your API key)
  

## Setup

### 1. Install Dependencies

First, install the required libraries using `pip`:

pip install apscheduler google-generativeai requests pandas

### 2. API Keys and Email Credentials

You will need to provide the following credentials:

- **Google Generative AI API Key**: You can obtain this from your Google Cloud console. 
- **Mailgun API Key**: Available after signing up with Mailgun.
- **Sender Email**: Your verified email address for sending emails.


## Code Explanation

### 1. **Installing Required Libraries**

We install the necessary libraries using pip. These include:

- **apscheduler**: For scheduling tasks.
- **google-generativeai**: For generating personalized email content.
- **requests**: For making HTTP requests to Mailgun API to send emails.
- **pandas**: For reading data from the CSV file.
  
!pip install apscheduler google-generativeai requests pandas


### 2. **Google Generative AI Setup**

To use Google’s Generative AI model, we configure it with your **Google API Key**. The model is set to **gemini-1.5-flash**, which generates text based on a given prompt.

GOOGLE_API_KEY = getpass("Enter Your GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


### 3. **Mailgun Configuration**

Mailgun is used to send emails. You need to configure your **Mailgun domain** and **API key**. Additionally, provide the sender’s verified email address.

MAILGUN_DOMAIN = "sandboxebda028ae0be440e91cd3cde71bac24c.mailgun.org"
MAILGUN_API_KEY = getpass("Enter Your Mailgun API Key: ")
sender_email = input("Enter Your Verified Email ID: ")


### 4. **Reading Recipient Data**

We use **pandas** to read a CSV file that contains the recipient details such as **email addresses**, **names**, and **attachment file paths**. The CSV file should have the following columns:
- `EMAIL_ID`: Recipient email address
- `NAME`: Name of the recipient
- `Files_to_be_attached`: File paths of the attachments to be sent

df = pd.read_csv(r"C:\path_to_file\sample_data1.csv")
receivers_email = df["EMAIL_ID"].values
attach_files = df["Files_to_be_attached"].values
names = df["NAME"].values


### 5. **Generating Email Content Using AI**

We create a function `generate_email_content()` that uses the **Google Generative AI** model to generate personalized content for each recipient based on their name.

def generate_email_content(name):
    prompt = f"Write a friendly email message for {name}..."
    response = model.generate_content(prompt)
    return response.text

### 6. **Sending Emails Using Mailgun**

We define a function `send_email_with_mailgun()` that sends the email using the **Mailgun API**. The function accepts the recipient’s email, the generated email content, and the attachment path as arguments. It handles the email sending process and handles any errors gracefully.


def send_email_with_mailgun(email, content, attachment_path, file_id):
    # Prepare data for the request
    ...
    # Send the request to Mailgun API
    response = requests.post(url, auth=("api", MAILGUN_API_KEY), data=data, files=files)

### 7. **Scheduling Emails**

We use **apscheduler**'s `BackgroundScheduler` to schedule the email sending. The `send_scheduled_emails()` function is executed at a specified time every day (e.g., 9:00 AM) to send emails.

scheduler = BackgroundScheduler()
scheduler.add_job(send_scheduled_emails, 'cron', hour=10, minute=57)
scheduler.start()

### 8. **Throttling Email Sending**

To avoid overloading the email system and maintain a steady flow, we introduce a delay of 10 seconds between each email by using `time.sleep(10)`.

time.sleep(10)  # Delay for throttling


### 9. **Running the Scheduler**

Once everything is set up, the scheduler is started, and emails are sent according to the defined schedule.

print("Scheduler started. Emails will be sent as per the schedule.")



## How It Works

1. **Input**: You enter your **Google API Key**, **Mailgun API Key**, and **sender email address**. The **CSV file** containing recipient information is loaded into the program.
2. **Content Generation**: For each recipient, the system generates personalized email content using Google’s Generative AI.
3. **Email Sending**: The email, along with an attachment (if provided), is sent via the Mailgun API.
4. **Scheduling**: The process is scheduled to run automatically at specified times using **apscheduler**.
5. **Throttling**: Emails are sent at a controlled rate by introducing a delay between them.

---


## Conclusion

This project demonstrates how to automate email sending, content generation, and scheduling using modern technologies. The integration of **Google Generative AI** and **Mailgun API** makes this application 
powerful and flexible. The use of **apscheduler** ensures that emails are sent at the right time, and **throttling** prevents overloading the system.

