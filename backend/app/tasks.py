from celery import shared_task
from app.workers import celery
from celery.schedules import crontab
from flask import render_template
from jinja2 import Template
from app.models import User


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=20, minute=51), 
        reminder_email.s('testcreator@gmail.com', 'Reminder Email'), 
        name='add every day'
    )

    sender.add_periodic_task(
        crontab(hour=13, minute=0, day_of_month='1'), 
        send_report.s(), 
        name='add every month'
    )

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = 'aryan@study.iitm.ac.in'
SENDER_PASSWORD = ''


def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

@shared_task(ignore_result=True)
def reminder_email(to, subject):
    users = User.query.all()
    for user in users:
        with open('test.html', 'r') as f:
            template = Template(f.read())
            send_message(user.email, subject,
                         template.render(email=user.email))
    return "OK"
    return True

@celery.task()
def send_report():
    pass
    return



@shared_task(ignore_result=True)
def say_hello():
    return "Hello"