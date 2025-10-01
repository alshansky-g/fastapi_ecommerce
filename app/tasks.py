from app.celery import celery


@celery.task
def call_background_task(message):
    print("Background Task called!")
    print(message)
