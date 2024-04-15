import smtplib
import flask_excel as excel
from celery import shared_task
from jinja2 import Template
from app.models import User
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.models import *
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
    return "Daily Reminder Sent!"

@shared_task(ignore_result=True)
def monthly_activity_report():
    template_str = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Activity Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #333;
            margin-top: 0;
        }
        p {
            color: #666;
            margin-bottom: 10px;
        }
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        ul li {
            margin-bottom: 5px;
        }
        .signature {
            margin-top: 20px;
            font-style: italic;
            color: #999;
            border-top: 1px solid #ccc;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Monthly Activity Report</h2>
        <p>Hello {{ user.firstname }},</p>
        <p>Here is your monthly activity report for {{ month }} {{ year }}:</p>
        <p>Total songs uploaded: {{ total_songs_uploaded }}</p>
        <p>Total albums uploaded: {{ total_albums_uploaded }}</p>
        <p>Total ratings received: {{ total_ratings_received }}</p>
        <p>List of songs:</p>
        <ul>
            {% for song in songs %}
            <li>{{ song.title }}</li>
            {% endfor %}
        </ul>
        <p>Average creator rating: {{ average_creator_rating }}</p>
        <div class="signature">
            <p>Best regards,</p>
            <p>Music Streaming Application Team</p>
        </div>
    </div>
</body>
</html>


    """

    template = Template(template_str)

    # Get the current month and year
    ist = timezone('Asia/Kolkata')
    now = datetime.now(ist)
    month = now.strftime("%B")
    year = now.strftime("%Y")

    creators = User.query.filter_by(user_type='creator').all()
    for creator in creators:
        # Calculate the start and end of the current month
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date.replace(month=start_date.month + 1) - timedelta(days=1)

        # Filter songs, albums, and ratings based on the creation, update, and rating dates within the current month
        songs = Song.query.filter(
            (Song.artist_id == creator.id) &
            (Song.upload_date >= start_date) &
            (Song.upload_date <= end_date)
        ).all()
        total_songs_uploaded = len(songs)

        albums = Album.query.filter(
            (Album.artist_id == creator.id) &
            (Album.creation_date >= start_date) &
            (Album.creation_date <= end_date)
        ).all()
        total_albums_uploaded = len(albums)

        ratings = Rating.query.filter(
            (Rating.user_id == creator.id) &
            (Rating.rating_date >= start_date) &
            (Rating.rating_date <= end_date)
        ).all()
        total_ratings_received = len(ratings)

        # Calculate the average creator rating
        creator_rating_sum = sum(rating.value for rating in ratings)
        average_creator_rating = creator_rating_sum / total_songs_uploaded if total_songs_uploaded != 0 else 0

        render_template = template.render(
            user=creator,
            month=month,
            year=year,
            total_songs_uploaded=total_songs_uploaded,
            total_albums_uploaded=total_albums_uploaded,
            total_ratings_received=total_ratings_received,
            songs=songs,
            average_creator_rating=average_creator_rating
        )
        send_email(creator.email, f"Monthly Activity Report - {month} {year}", render_template)

    return "Monthly activity report sent successfully."


@shared_task(ignore_result=False)
def create_csv():
        user_data = User.query.with_entities(User.firstname, User.lastname, User.email, User.is_blacklisted).all()
        output_csv = excel.make_response_from_query_sets(user_data, column_names=["firstname", "lastname", "email", "is_blacklisted"], file_type='csv')
        filename = "users.csv"

        with open(filename, "wb") as f:
            f.write(output_csv.data)

        return filename
