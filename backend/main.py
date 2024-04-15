from app import create_app
from app.workers import celery_init_app
from celery.schedules import crontab
from app.tasks import daily_reminder, monthly_activity_report

app = create_app()
celery = celery_init_app(app)



@celery.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=13, minute=00),
        daily_reminder.s('Daily Reminder!'),
    )

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Add a periodic task to run the monthly_activity_report task on the first day of every month
    sender.add_periodic_task(
        crontab(day_of_month=1 ,hour=13, minute=00),
        monthly_activity_report.s(),
    )


if __name__ == '__main__':

    app.run(debug=True)
