# # from flask import Flask, request, jsonify, render_template, send_from_directory
# # import sqlite3
# # import os
# # from apscheduler.schedulers.background import BackgroundScheduler
# # import requests  # For Mailgun API
# # from datetime import datetime
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_cors import CORS

# # app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# # # Initialize database
# # DATABASE = "emails.db"

# # def get_db_connection():
# #     conn = sqlite3.connect(DATABASE)
# #     conn.row_factory = sqlite3.Row
# #     return conn



# # def create_database():
# #     conn = sqlite3.connect("emails.db")  # Create 'emails.db' in the project directory
# #     cursor = conn.cursor()
# #     cursor.execute(
# #         """
# #         CREATE TABLE IF NOT EXISTS emails (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             recipient TEXT NOT NULL,
# #             subject TEXT NOT NULL,
# #             body TEXT NOT NULL,
# #             scheduled_time TEXT NOT NULL,
# #             status TEXT NOT NULL
# #         )
# #          """
# #     )
# #     conn.commit()
# #     conn.close()

# # # Call the function before starting the app
# # create_database()

# # # Serve the frontend
# # @app.route("/")
# # def index():
# #     return render_template("index.html")

# # # API to schedule email
# # @app.route("/api/schedule", methods=["POST"])
# # def schedule_email():
# #     data = request.json
# #     recipient = data.get("recipient")
# #     subject = data.get("subject")
# #     body = data.get("body")
# #     scheduled_time = data.get("scheduled_time")

# #     # Save to DB
# #     conn = get_db_connection()
# #     conn.execute(
# #         "INSERT INTO emails (recipient, subject, body, scheduled_time, status) VALUES (?, ?, ?, ?, ?)",
# #         (recipient, subject, body, scheduled_time, "Scheduled"),
# #     )
# #     conn.commit()
# #     conn.close()

# #     return jsonify({"message": "Email scheduled successfully!"}), 200

# # # API to fetch analytics
# # @app.route("/api/analytics", methods=["GET"])
# # def analytics():
# #     conn = get_db_connection()
# #     total_sent = conn.execute("SELECT COUNT(*) FROM emails WHERE status = 'Sent'").fetchone()[0]
# #     total_failed = conn.execute("SELECT COUNT(*) FROM emails WHERE status = 'Failed'").fetchone()[0]
# #     total_scheduled = conn.execute("SELECT COUNT(*) FROM emails WHERE status = 'Scheduled'").fetchone()[0]
# #     conn.close()

# #     analytics_data = {
# #         "total_sent": total_sent,
# #         "total_failed": total_failed,
# #         "total_scheduled": total_scheduled,
# #     }
# #     return jsonify(analytics_data)

# # # Email sending function (used with APScheduler)
# # def send_email(recipient, subject, body):
# #     # Use Mailgun or other API here
# #     try:
# #         response = requests.post(
# #             "https://api.mailgun.net/v3/sandboxe007be8ff90748f0959dd49c96ba67c9.mailgun.org/messages",
# #             auth=("api", "4daacef91076afadf347a22a04c334b8-79295dd0-35fe5d3b"),
# #             data={
# #                 "from": "Your Name <your-email@example.com>",
# #                 "to": recipient,
# #                 "subject": subject,
# #                 "text": body,
# #             },
# #         )
# #         status = "Sent" if response.status_code == 200 else "Failed"
# #     except Exception as e:
# #         status = "Failed"

# #     # Update database with email status
# #     conn = get_db_connection()
# #     conn.execute(
# #         "UPDATE emails SET status = ? WHERE recipient = ? AND subject = ?",
# #         (status, recipient, subject),
# #     )
# #     conn.commit()
# #     conn.close()

# # # Scheduler to send emails at scheduled times
# # scheduler = BackgroundScheduler()
# # scheduler.start()

# # @app.before_first_request
# # def start_scheduled_tasks():
# #     conn = get_db_connection()
# #     rows = conn.execute("SELECT * FROM emails WHERE status = 'Scheduled'").fetchall()
# #     conn.close()

# #     for row in rows:
# #         scheduled_time = datetime.strptime(row["scheduled_time"], "%Y-%m-%d %H:%M:%S")
# #         scheduler.add_job(
# #             send_email,
# #             "date",
# #             run_date=scheduled_time,
# #             args=[row["recipient"], row["subject"], row["body"]],
# #         )



# # # first_request = True 
# # # @app.before_request 
# # # def start_scheduled_tasks(): 
# # #     global first_request 
# # #     if first_request: 
# # #         first_request = False
# # #         conn = get_db_connection()
# # #         rows = conn.execute("SELECT * FROM emails WHERE status = 'Scheduled'").fetchall()
# # #         conn.close()

# # #         for row in rows: 
# # #             scheduled_time = datetime.strptime(row["scheduled_time"], "%Y-%m-%d %H:%M:%S") 
# # #             scheduler.add_job( 
# # #                 send_email,
# # #                 "date",
# # #                 run_date=scheduled_time,
# # #                 args=[row["recipient"], row["subject"], row["body"]],
# # #             )    

# # if __name__ == "__main__":
# #     app.run(debug=True)






# from flask import Flask, jsonify, request, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from datetime import datetime
# import os

# app = Flask(__name__, static_folder='frontend')
# CORS(app)  # Enable CORS for all routes

# # Configure the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Database model
# class EmailStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     recipient = db.Column(db.String(100), nullable=False)  #check it ""
#     status = db.Column(db.String(20), nullable=False)
#     sent_at = db.Column(db.DateTime, nullable=True)
#     scheduled_at = db.Column(db.DateTime, nullable=True)
#     response_received = db.Column(db.Boolean, default=False)
#     message_id = db.Column(db.String(100), unique=True, nullable=True)  # Mailgun Message ID

#     def __repr__(self):
#         return f'<EmailStatus {self.recipient} - {self.status}>'

# # Initialize the database
# # @app.before_first_request
# # def create_tables():
# #     db.create_all()

# # Ensure database tables are created at the app startup
# @app.before_request
# def initialize_database():
#     if not os.path.exists('emails.db'):
#         with app.app_context():
#             db.create_all()



# # API endpoint to get analytics
# @app.route('/api/analytics', methods=['GET'])
# def get_analytics():
#     total_sent = EmailStatus.query.filter_by(status="sent").count()
#     total_pending = EmailStatus.query.filter_by(status="pending").count()
#     total_scheduled = EmailStatus.query.filter_by(status="scheduled").count()
#     total_failed = EmailStatus.query.filter_by(status="failed").count()
#     total_response = EmailStatus.query.filter_by(response_received=True).count()
#     response_rate = (total_response / total_sent * 100) if total_sent > 0 else 0

#     return jsonify({
#         "total_sent": total_sent,
#         "total_pending": total_pending,
#         "total_scheduled": total_scheduled,
#         "total_failed": total_failed,
#         "response_rate": response_rate
#     })

# # Webhook endpoint to receive Mailgun events
# @app.route('/webhook/mailgun', methods=['POST'])
# def mailgun_webhook():
#     event_data = request.form
#     event = event_data.get('event-data', {})
#     event_type = event.get('event')
#     message_id = event.get('message', {}).get('headers', {}).get('message-id')
#     recipient = event.get('recipient')

#     # Find the email in the database by message_id
#     email = EmailStatus.query.filter_by(message_id=message_id).first()

#     if not email:
#         return jsonify({"status": "Email not found"}), 404

#     # Update email status based on event type
#     if event_type == 'delivered':
#         email.status = 'sent'
#         email.sent_at = datetime.utcnow()
#     elif event_type == 'failed':
#         email.status = 'failed'
#     elif event_type == 'opened':
#         email.response_received = True
#     elif event_type == 'clicked':
#         email.response_received = True
#     # Add more event types as needed

#     db.session.commit()
#     return jsonify({"status": "success"}), 200

# # Serve front-end files
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def serve_frontend(path):
#     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
import threading
import schedule
import time
import requests  # For Mailgun API
import sqlite3


app = Flask(__name__, static_folder='frontend')
CORS(app)  # Enable CORS for all routes

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class EmailStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    scheduled_at = db.Column(db.DateTime, nullable=True)
    response_received = db.Column(db.Boolean, default=False)
    message_id = db.Column(db.String(100), unique=True, nullable=True)

    def __repr__(self):
        return f'<EmailStatus {self.recipient} - {self.status}>'

# Initialize the database
@app.before_request
def initialize_database():
    if not os.path.exists('emails.db'):
        with app.app_context():
            db.create_all()

# Email sending function (used with APScheduler)
def send_email(recipient, subject, body):
    # Use Mailgun or other API here
    try:
        response = requests.post(
            "https://api.mailgun.net/v3/sandboxe007be8ff90748f0959dd49c96ba67c9.mailgun.org/messages",
            auth=("api", "4daacef91076afadf347a22a04c334b8-79295dd0-35fe5d3b"),
            data={
                "from": "Your Name <your-email@example.com>",
                "to": recipient,
                "subject": subject,
                "text": body,
            },
        )
        status = "Sent" if response.status_code == 200 else "Failed"
    except Exception as e:
        status = "Failed"

    # Update database with email status
    email = EmailStatus.query.filter_by(recipient=recipient, subject=subject).first()
    if email:
        email.status = status
        email.sent_at = datetime.utcnow()
        db.session.commit()

# Scheduler to send emails at scheduled times
def send_scheduled_emails():
    # Logic to send emails from scheduled tasks
    conn = sqlite3.connect("emails.db")  # Replace with SQLAlchemy session if needed
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM emails WHERE status = 'Scheduled'").fetchall()
    conn.close()

    for row in rows:
        scheduled_time = datetime.strptime(row['scheduled_time'], "%Y-%m-%d %H:%M:%S")
        if scheduled_time <= datetime.utcnow():
            send_email(row['recipient'], row['subject'], row['body'])

def run_scheduler():
    schedule.every(10).seconds.do(send_scheduled_emails)
    while True:
        schedule.run_pending()
        time.sleep(1)

# @app.before_first_request
# def start_scheduler():
#     # Run the scheduler in a separate thread to not block the Flask app
#     threading.Thread(target=run_scheduler, daemon=True).start()

scheduler_started = False

@app.before_request
def start_scheduler():
    global scheduler_started
    if not scheduler_started:
        threading.Thread(target=run_scheduler, daemon=True).start()
        scheduler_started = True


# API endpoint to get analytics
@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    total_sent = EmailStatus.query.filter_by(status="sent").count()
    total_pending = EmailStatus.query.filter_by(status="pending").count()
    total_scheduled = EmailStatus.query.filter_by(status="scheduled").count()
    total_failed = EmailStatus.query.filter_by(status="failed").count()
    total_response = EmailStatus.query.filter_by(response_received=True).count()
    response_rate = (total_response / total_sent * 100) if total_sent > 0 else 0

    return jsonify({
        "total_sent": total_sent,
        "total_pending": total_pending,
        "total_scheduled": total_scheduled,
        "total_failed": total_failed,
        "response_rate": response_rate
    })

# Webhook endpoint to receive Mailgun events
@app.route('/webhook/mailgun', methods=['POST'])
def mailgun_webhook():
    event_data = request.form
    event = event_data.get('event-data', {})
    event_type = event.get('event')
    message_id = event.get('message', {}).get('headers', {}).get('message-id')
    recipient = event.get('recipient')

    # Find the email in the database by message_id
    email = EmailStatus.query.filter_by(message_id=message_id).first()

    if not email:
        return jsonify({"status": "Email not found"}), 404

    # Update email status based on event type
    if event_type == 'delivered':
        email.status = 'sent'
        email.sent_at = datetime.utcnow()
    elif event_type == 'failed':
        email.status = 'failed'
    elif event_type == 'opened':
        email.response_received = True
    elif event_type == 'clicked':
        email.response_received = True
    # Add more event types as needed

    db.session.commit()
    return jsonify({"status": "success"}), 200

# Serve front-end files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
