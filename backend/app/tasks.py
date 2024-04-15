from celery import shared_task
from jinja2 import Template
from app.models import User
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from email.mime.image import MIMEImage
from app.models import User
from datetime import datetime, timedelta
from pytz import timezone


def send_email(to_address, subject, content_body, attachment=None, images=None, filename=None, subtype=None):
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "testadmin@gmail.com"
    SENDER_PASSWORD = ""

    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(content_body, "html"))

    if attachment:
        part = MIMEApplication(attachment.read(), _subtype=subtype)
        part.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(part)

    sm = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    sm.login(SENDER_ADDRESS, SENDER_PASSWORD)
    sm.send_message(msg)
    sm.quit()


@shared_task(ignore_result=True)
def daily_reminder(subject):
    template_str = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reminder to Visit Music Streaming Application</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #333;
        }
        p {
            color: #666;
        }
        .signature {
            margin-top: 20px;
            font-style: italic;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Reminder to Visit Music Streaming Application</h2>
        <p>Dear {{ user }},</p>
        <p>It seems it's been a while since you last visited our music streaming application.</p>
        <p>We wanted to remind you that there's a lot of great music waiting for you to discover. Come back and explore the latest releases, create playlists, and enjoy your favorite tracks.</p>
        <p>Your presence on our platform matters to us, and we look forward to welcoming you back soon.</p>
        <div class="signature">
            <p>Best regards,</p>
            <p>{{ your_name }}</p>
        </div>
    </div>
</body>
</html>

        """
    template = Template(template_str)
    ist = timezone('Asia/Kolkata')
    now = datetime.now(ist)
    users = User.query.filter(
        (User.last_visit < now - timedelta(days=1)) | (User.last_visit == None)).all()
    for user in users:
        render_template = template.render(user=f"{user.firstname} {user.lastname}", your_name="Music Streaming Application Team")
        send_email(user.email, subject, render_template)
    return "OK"
