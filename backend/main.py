from app import create_app
from app.workers import celery_init_app
from app.tasks import test

app = create_app()
celery = celery_init_app(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    
if __name__ == '__main__':

    app.run(debug=True)
