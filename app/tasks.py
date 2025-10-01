import time

from app.celery import celery


@celery.task
def call_background_task(message, delay=5):
    time.sleep(delay)
    print(f"Background Task called! Delay is {delay}s")
    print(message)
