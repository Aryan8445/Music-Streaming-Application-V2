from celery import shared_task
from celery.schedules import crontab



@shared_task(ignore_result=False)
def test(arg):
    print(arg)
    return "Hello World!"



@shared_task(ignore_result=False)
def add_together():
    print("Hello World!")
    return "Hello World!"

