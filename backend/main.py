from app import create_app
from app.workers import celery_init_app
from celery.schedules import crontab
from app.tasks import daily_reminder

app = create_app()
celery = celery_init_app(app)



@celery.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=11, minute=50),
        daily_reminder.s('Daily Reminder!'),
    )

if __name__ == '__main__':

    app.run(debug=True)
